from django.db.models import Sum, Count, Avg, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from ..models import Tache, ActiviteTache, Machine, ActiviteTachePieceDetachee
from datetime import datetime
from rest_framework.exceptions import ValidationError

class DashboardStatsView(APIView):
    def get(self, request):
        # Récupération des paramètres de date
        date_debut = request.query_params.get('date_debut', None)
        date_fin = request.query_params.get('date_fin', None)
        
        # Filtre de base pour les tâches non supprimées
        taches_query = Tache.objects.filter(deleted_at__isnull=True)
        
        # Application des filtres de date si présents
        if date_debut:
            taches_query = taches_query.filter(date_debut__gte=date_debut)
        if date_fin:
            taches_query = taches_query.filter(date_fin__lte=date_fin)
        
        # Récupération des IDs des tâches filtrées
        tache_ids = list(taches_query.values_list('id', flat=True))
        
        # Nombre total de tâches filtrées
        total_taches = len(tache_ids)
        
        # Nombre total d'activités pour les tâches filtrées
        total_activites = ActiviteTache.objects.filter(
            tache_id__in=tache_ids, 
            deleted_at__isnull=True
        ).count()
        
        # Calcul du temps total passé
        temps_total = ActiviteTache.objects.filter(
            tache_id__in=tache_ids,
            deleted_at__isnull=True
        ).aggregate(
            total_heures=Sum('temps_passe_heure', default=0),
            total_minutes=Sum('temps_passe_minute', default=0)
        )
        
        # Conversion et formatage du temps
        total_h = temps_total['total_heures'] + (temps_total['total_minutes'] // 60)
        total_m = temps_total['total_minutes'] % 60
        temps_total_str = f"{total_h}h {total_m}mn"
        
        # Calcul du temps moyen
        if total_taches > 0:
            avg_h = total_h // total_taches
            avg_m = (total_m + (total_h % total_taches * 60)) // total_taches
            temps_moyen_str = f"{avg_h}h {avg_m}mn"
        else:
            temps_moyen_str = "0h 0mn"
        
        data = {
            'total_taches': total_taches,
            'total_activites': total_activites,
            'temps_total_passe': temps_total_str,
            'temps_moyen_passe': temps_moyen_str,
            # 'filtres': {
            #     'date_debut': date_debut,
            #     'date_fin': date_fin
            # }
        }
        
        return Response(data, status=status.HTTP_200_OK)
    
    
class BaseStatsMixin:
    @staticmethod
    def calculate_percentage(values):
        total = sum(values)
        if total == 0:
            return [0] * len(values)
        return [round((v / total) * 100, 2) for v in values]
    
    
class BaseStatsView(APIView, BaseStatsMixin):
    def validate_date(self, date_str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            raise ValidationError("Format de date invalide. Utilisez YYYY-MM-DD")

    def get_date_filtered_taches(self, request):
        date_debut = request.query_params.get('date_debut', None)
        date_fin = request.query_params.get('date_fin', None)

        # Validation des dates
        if date_debut:
            date_debut = self.validate_date(date_debut)
        if date_fin:
            date_fin = self.validate_date(date_fin)

        taches_query = Tache.objects.filter(deleted_at__isnull=True)

        if date_debut and date_fin:
            taches_query = taches_query.filter(
                Q(date_debut__gte=date_debut) & 
                Q(date_fin__lte=date_fin)
            )
        elif date_debut:
            taches_query = taches_query.filter(date_debut__gte=date_debut)
        elif date_fin:
            taches_query = taches_query.filter(date_fin__lte=date_fin)

        return taches_query

class TopTachesStatsView(BaseStatsView):
    def get(self, request):
        filter_type = request.query_params.get('filter', 'temps')
        try:
            taches_query = self.get_date_filtered_taches(request)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if filter_type == 'temps':
            return self.get_top_by_time(taches_query)
        elif filter_type == 'count':
            return self.get_top_by_activity_count(taches_query)
        elif filter_type == 'cout':
            return self.get_top_by_cost(taches_query)
        else:
            return Response(
                {"error": "Filtre invalide. Options: temps, count, cout"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_top_by_time(self, taches_query):
        tache_data = []
        for tache in taches_query:
            activites = ActiviteTache.objects.filter(
                tache=tache, 
                deleted_at__isnull=True
            )
            total_h = sum(a.temps_passe_heure or 0 for a in activites)
            total_m = sum(a.temps_passe_minute or 0 for a in activites)
            total_minutes = total_h * 60 + total_m
            tache_data.append({
                'id': tache.id,
                'nom': tache.nom_tache,
                'valeur': total_minutes
            })

        tache_data_sorted = sorted(tache_data, key=lambda x: x['valeur'], reverse=True)[:10]
        values = [item['valeur'] for item in tache_data_sorted]
        percentages = self.calculate_percentage(values)

        response_data = []
        for i, item in enumerate(tache_data_sorted):
            hours = item['valeur'] // 60
            minutes = item['valeur'] % 60
            response_data.append({
                'id': item['id'],
                'nom': item['nom'],
                'valeur': f"{hours}h {minutes}mn",
                'pourcentage': percentages[i]
            })

        return Response(response_data, status=status.HTTP_200_OK)

    def get_top_by_activity_count(self, taches_query):
        tache_data = []
        for tache in taches_query:
            count = ActiviteTache.objects.filter(
                tache=tache,
                deleted_at__isnull=True
            ).count()
            tache_data.append({
                'id': tache.id,
                'nom': tache.nom_tache,
                'valeur': count
            })

        tache_data_sorted = sorted(tache_data, key=lambda x: x['valeur'], reverse=True)[:10]
        values = [item['valeur'] for item in tache_data_sorted]
        percentages = self.calculate_percentage(values)

        response_data = []
        for i, item in enumerate(tache_data_sorted):
            response_data.append({
                'id': item['id'],
                'nom': item['nom'],
                'valeur': item['valeur'],
                'pourcentage': percentages[i]
            })

        return Response(response_data, status=status.HTTP_200_OK)

    def get_top_by_cost(self, taches_query):
        tache_data = []
        for tache in taches_query:
            total_cost = Decimal(0)
            activites = ActiviteTache.objects.filter(
                tache=tache,
                deleted_at__isnull=True
            )
            for activite in activites:
                pieces = ActiviteTachePieceDetachee.objects.filter(activite_tache=activite)
                for piece in pieces:
                    prix = piece.prix_piece_detachees or Decimal(0)
                    quantite = piece.quantite or 0
                    total_cost += Decimal(prix) * Decimal(quantite)

            tache_data.append({
                'id': tache.id,
                'nom': tache.nom_tache,
                'valeur': float(total_cost)
            })

        tache_data_sorted = sorted(tache_data, key=lambda x: x['valeur'], reverse=True)[:10]
        values = [item['valeur'] for item in tache_data_sorted]
        percentages = self.calculate_percentage(values)

        response_data = []
        for i, item in enumerate(tache_data_sorted):
            response_data.append({
                'id': item['id'],
                'nom': item['nom'],
                'valeur': item['valeur'],
                'pourcentage': percentages[i]
            })

        return Response(response_data, status=status.HTTP_200_OK)

class TopMachinesStatsView(BaseStatsView):
    def get(self, request):
        filter_type = request.query_params.get('filter', 'temps')
        try:
            taches_query = self.get_date_filtered_taches(request)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if filter_type == 'temps':
            return self.get_top_by_time(taches_query)
        elif filter_type == 'count':
            return self.get_top_by_activity_count(taches_query)
        elif filter_type == 'cout':
            return self.get_top_by_cost(taches_query)
        else:
            return Response(
                {"error": "Filtre invalide. Options: temps, count, cout"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_top_by_time(self, taches_query):
        machine_data = []
        machines = Machine.objects.filter(
            id__in=taches_query.values_list('machine', flat=True).distinct(),
            deleted_at__isnull=True
        )

        for machine in machines:
            machine_taches = taches_query.filter(machine=machine)
            total_minutes = 0
            
            for tache in machine_taches:
                activites = ActiviteTache.objects.filter(
                    tache=tache,
                    deleted_at__isnull=True
                )
                total_h = sum(a.temps_passe_heure or 0 for a in activites)
                total_m = sum(a.temps_passe_minute or 0 for a in activites)
                total_minutes += total_h * 60 + total_m
            
            machine_data.append({
                'id': machine.id,
                'numero_machine' : machine.numero_machine,
                'nom': machine.nom_machine,
                'numero_de_serie': machine.numero_de_serie,
                'valeur': total_minutes
            })

        machine_data_sorted = sorted(machine_data, key=lambda x: x['valeur'], reverse=True)[:10]
        values = [item['valeur'] for item in machine_data_sorted]
        percentages = self.calculate_percentage(values)

        response_data = []
        for i, item in enumerate(machine_data_sorted):
            hours = item['valeur'] // 60
            minutes = item['valeur'] % 60
            total_minutes = item['valeur']
            response_data.append({
                'id': item['id'],
                'numero_machine': item['numero_machine'],
                'nom': item['nom'],
                'numero_de_serie': item['numero_de_serie'],
                'valeur': f"{hours}h {minutes}mn",
                'total_minutes': total_minutes,
                'pourcentage': percentages[i]
            })

        return Response(response_data, status=status.HTTP_200_OK)

    def get_top_by_activity_count(self, taches_query):
        machine_data = []
        machines = Machine.objects.filter(
            id__in=taches_query.values_list('machine', flat=True).distinct(),
            deleted_at__isnull=True
        )

        for machine in machines:
            count = ActiviteTache.objects.filter(
                tache__in=taches_query.filter(machine=machine),
                deleted_at__isnull=True
            ).count()
            
            machine_data.append({
                'id': machine.id,
                'numero_machine' : machine.numero_machine,
                'nom': machine.nom_machine,
                'numero_de_serie': machine.numero_de_serie,
                'valeur': count
            })

        machine_data_sorted = sorted(machine_data, key=lambda x: x['valeur'], reverse=True)[:10]
        values = [item['valeur'] for item in machine_data_sorted]
        percentages = self.calculate_percentage(values)

        response_data = []
        for i, item in enumerate(machine_data_sorted):
            response_data.append({
                'id': item['id'],
                'numero_machine': item['numero_machine'],
                'nom': item['nom'],
                'numero_de_serie': item['numero_de_serie'],
                'valeur': item['valeur'],
                'pourcentage': percentages[i]
            })

        return Response(response_data, status=status.HTTP_200_OK)

    def get_top_by_cost(self, taches_query):
        machine_data = []
        machines = Machine.objects.filter(
            id__in=taches_query.values_list('machine', flat=True).distinct(),
            deleted_at__isnull=True
        )

        for machine in machines:
            total_cost = Decimal(0)
            machine_taches = taches_query.filter(machine=machine)
            
            for tache in machine_taches:
                activites = ActiviteTache.objects.filter(
                    tache=tache,
                    deleted_at__isnull=True
                )
                for activite in activites:
                    pieces = ActiviteTachePieceDetachee.objects.filter(activite_tache=activite)
                    for piece in pieces:
                        prix = piece.prix_piece_detachees or Decimal(0)
                        quantite = piece.quantite or 0
                        total_cost += Decimal(prix) * Decimal(quantite)
            
            machine_data.append({
                'id': machine.id,
                'numero_machine': machine.numero_machine,
                'nom': machine.nom_machine,
                'numero_de_serie': machine.numero_de_serie,
                'valeur': float(total_cost)
            })

        machine_data_sorted = sorted(machine_data, key=lambda x: x['valeur'], reverse=True)[:10]
        values = [item['valeur'] for item in machine_data_sorted]
        percentages = self.calculate_percentage(values)

        response_data = []
        for i, item in enumerate(machine_data_sorted):
            response_data.append({
                'id': item['id'],
                'numero_machine': item['numero_machine'],
                'nom': item['nom'],
                'numero_de_serie': item['numero_de_serie'],
                'valeur': item['valeur'],
                'pourcentage': percentages[i]
            })

        return Response(response_data, status=status.HTTP_200_OK)