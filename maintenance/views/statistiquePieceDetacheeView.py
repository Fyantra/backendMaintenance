from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Q, F
from datetime import datetime
from ..models import (
    PieceDetachee, 
    HistoriqueMouvementPieceDetachee,
    ReapprovisionnementPieceDetachee,
)

class PieceDetacheeStatsView(APIView):
    def get(self, request):
        # Récupération des paramètres de filtre
        piece_detachee_id = request.query_params.get('piece_detachee_id', None)
        machine_ids = request.query_params.getlist('machine_ids[]', [])
        emplacement_ids = request.query_params.getlist('emplacement_ids[]', [])
        date_debut = request.query_params.get('date_debut', None)
        date_fin = request.query_params.get('date_fin', None)
        
        # Conversion des dates
        try:
            date_debut = self._parse_date(date_debut) if date_debut else None
            date_fin = self._parse_date(date_fin) if date_fin else None
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filtre de base pour les pièces
        piece_filter = Q()
        if emplacement_ids:
            piece_filter &= Q(emplacement_id__in=emplacement_ids)
        if piece_detachee_id:
            piece_filter &= Q(id=piece_detachee_id)

        # Vérifier si des pièces correspondent aux filtres
        if not PieceDetachee.objects.filter(piece_filter, deleted_at__isnull=True).exists():
            return self._empty_response(piece_detachee_id is not None)

        # Mode de fonctionnement
        if piece_detachee_id:
            return self._get_single_piece_stats(piece_detachee_id, machine_ids, emplacement_ids, date_debut, date_fin)
        else:
            return self._get_all_pieces_stats(machine_ids, emplacement_ids, date_debut, date_fin)
        
    def _parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Format de date invalide. Utilisez YYYY-MM-DD.")
    
    def _empty_response(self, is_single_piece):
        """Retourne une réponse vide"""
        if is_single_piece:
            return Response({
                'piece_detachee': None,
                'valorisation_stock': 0,
                'quantite_totale_sortie_brut': 0,
                'cout_total_sortie_brut': 0,
                'quantite_totale_sortie_net': 0,
                'cout_total_sortie_net': 0,
                'quantite_totale_reappro': 0,
                'cout_total_reappro': 0,
            })
        else:
            return Response({
                'global_stats': {
                    'valorisation_stock': 0,
                    'quantite_totale_sortie_brut': 0,
                    'cout_total_sortie_brut': 0,
                    'quantite_totale_sortie_net': 0,
                    'cout_total_sortie_net': 0,
                    'quantite_totale_reappro': 0,
                    'cout_total_reappro': 0,
                },
                'pieces_stats': [],
            })

    def _get_single_piece_stats(self, piece_id, machine_ids, emplacement_ids, date_debut, date_fin):
        """Stats pour une seule pièce avec tous les filtres"""
        try:
            piece = PieceDetachee.objects.filter(deleted_at__isnull=True).get(id=piece_id)
            if emplacement_ids and piece.emplacement_id not in [int(id) for id in emplacement_ids]:
                return self._empty_response(True)
        except PieceDetachee.DoesNotExist:
            return self._empty_response(True)

        # Filtres pour les mouvements
        historique_filters = Q(piece_detachee_id=piece_id)
        reappro_filters = Q(pieces_detachees_id=piece_id)
        
        if machine_ids:
            historique_filters &= Q(tache__machine_id__in=machine_ids)
        
        if date_debut and date_fin:
            date_filter = Q(date_realisation__date__range=[date_debut, date_fin])
        elif date_debut:
            date_filter = Q(date_realisation__date__gte=date_debut)
        elif date_fin:
            date_filter = Q(date_realisation__date__lte=date_fin)
        else:
            date_filter = Q()

        historique_filters &= date_filter
        reappro_filters &= date_filter

        # Calcul des stats
        sortie_stats = self._calculate_sortie_stats(historique_filters)
        reappro_stats = self._calculate_reappro_stats(reappro_filters, machine_ids)

        return Response({
            'piece_detachee': {
                'id': piece.id,
                'nom': piece.nom_piecedetache,
                'code_article': piece.code_article,
                'emplacement': piece.emplacement.nom_atelier if piece.emplacement else None,
            },
            'valorisation_stock': float(piece.quantite * piece.prix_unitaire),
            **sortie_stats,
            **reappro_stats,
        })

    def _get_all_pieces_stats(self, machine_ids, emplacement_ids, date_debut, date_fin):
        """Stats pour toutes les pièces avec filtres"""
        # Filtre pour les pièces
        piece_filter = Q()
        if emplacement_ids:
            piece_filter &= Q(emplacement_id__in=emplacement_ids)
        
        pieces = PieceDetachee.objects.filter(piece_filter, deleted_at__isnull=True)
        
        # Filtres pour les mouvements
        base_historique_filters = Q()
        base_reappro_filters = Q()
        
        if machine_ids:
            base_historique_filters &= Q(tache__machine_id__in=machine_ids)
        
        if date_debut and date_fin:
            date_filter = Q(date_realisation__date__range=[date_debut, date_fin])
        elif date_debut:
            date_filter = Q(date_realisation__date__gte=date_debut)
        elif date_fin:
            date_filter = Q(date_realisation__date__lte=date_fin)
        else:
            date_filter = Q()

        base_historique_filters &= date_filter
        base_reappro_filters &= date_filter

        # Calcul des stats globales
        valorisation_stock = pieces.aggregate(
            total=Sum(F('quantite') * F('prix_unitaire'))
        )['total'] or 0
        
        # Calcul des stats de sortie (uniquement pour les pièces filtrées)
        sortie_stats = self._calculate_sortie_stats(
            base_historique_filters & Q(piece_detachee__in=pieces.values('id'))
        )
        
        # Calcul des stats de réappro (uniquement pour les pièces filtrées)
        reappro_stats = self._calculate_reappro_stats(
            base_reappro_filters & Q(pieces_detachees__in=pieces.values('id')),
            machine_ids
        )

        # Stats par pièce
        pieces_stats = []
        for piece in pieces:
            piece_stats = {
                'piece_detachee_id': piece.id,
                'piece_detachee_nom': piece.nom_piecedetache,
                'piece_detachee_code': piece.code_article,
                'emplacement': piece.emplacement.nom_atelier if piece.emplacement else None,
                'valorisation_stock': float(piece.quantite * piece.prix_unitaire),
                **self._calculate_sortie_stats(
                    base_historique_filters & Q(piece_detachee_id=piece.id)
                ),
                **self._calculate_reappro_stats(
                    base_reappro_filters & Q(pieces_detachees_id=piece.id),
                    machine_ids
                )
            }
            pieces_stats.append(piece_stats)

        return Response({
            'global_stats': {
                'valorisation_stock': float(valorisation_stock),
                **sortie_stats,
                **reappro_stats,
            },
            'pieces_stats': pieces_stats,
        })
        
    def _calculate_sortie_stats(self, filters):
        """Calcule les statistiques de sortie (consommations et retours)"""
        mouvements = HistoriqueMouvementPieceDetachee.objects.filter(
            filters,
            source__in=['Consommation', 'Retour de consommation']
        ).aggregate(
            # Brut (consommations seulement)
            quantite_brut=Sum('quantite', filter=Q(source='Consommation')),
            cout_brut=Sum('cout', filter=Q(source='Consommation')),
            
            # Retours seulement
            quantite_retour=Sum('quantite', filter=Q(source='Retour de consommation')),
            cout_retour=Sum('cout', filter=Q(source='Retour de consommation'))
        )
        
        # Calcul des valeurs brutes
        quantite_brut = abs(mouvements['quantite_brut'] or 0)
        cout_brut = abs(mouvements['cout_brut'] or 0)
        
        # Calcul des retours
        quantite_retour = abs(mouvements['quantite_retour'] or 0)
        cout_retour = abs(mouvements['cout_retour'] or 0)
        
        # Calcul des valeurs nettes
        quantite_net = quantite_brut - quantite_retour
        cout_net = cout_brut - cout_retour
        
        return {
            'quantite_totale_sortie_brut': quantite_brut,
            'cout_total_sortie_brut': float(cout_brut),
            'quantite_totale_sortie_net': quantite_net,
            'cout_total_sortie_net': float(cout_net),
            # 'quantite_retour': quantite_retour,
            # 'cout_retour': float(cout_retour),
        }
    
    def _calculate_reappro_stats(self, filters, machine_ids):
        """Calcule les statistiques de réapprovisionnement"""
        if machine_ids:
            return {
                'quantite_totale_reappro': 0,
                'cout_total_reappro': 0.0,
            }
        
        reappro = ReapprovisionnementPieceDetachee.objects.filter(
            filters
        ).aggregate(
            total_quantite=Sum('quantite'),
            total_cout=Sum(F('quantite') * F('prix_piece_detachees'))
        )
        
        return {
            'quantite_totale_reappro': reappro['total_quantite'] or 0,
            'cout_total_reappro': float(reappro['total_cout'] or 0),
        }