from django.core.management.base import BaseCommand
from agronegocio.models import Producer, Farm, Harvest, Crop
from django.db import transaction

class Command(BaseCommand):
    help = "Seed database with initial data"

    @transaction.atomic
    def handle(self, *args, **options):
        producers_data = [
            {"name": "Produtor A", "cpf_cnpj": "12345678900"},
            {"name": "Produtor B", "cpf_cnpj": "98765432100"},
            {"name": "Produtor C", "cpf_cnpj": "11122233344"},
            {"name": "Produtor D", "cpf_cnpj": "55566677788"},
            {"name": "Produtor E", "cpf_cnpj": "99988877766"},
            {"name": "Produtor F", "cpf_cnpj": "44455566677"},
            {"name": "Produtor G", "cpf_cnpj": "22233344455"},
            {"name": "Produtor H", "cpf_cnpj": "33344455566"},
            {"name": "Produtor I", "cpf_cnpj": "66677788899"},
            {"name": "Produtor J", "cpf_cnpj": "77788899900"},
            {"name": "Produtor K", "cpf_cnpj": "88899900011"},
            {"name": "Produtor L", "cpf_cnpj": "10101010101"},
            {"name": "Produtor M", "cpf_cnpj": "12121212121"},
            {"name": "Produtor N", "cpf_cnpj": "13131313131"},
            {"name": "Produtor O", "cpf_cnpj": "14141414141"},
            {"name": "Produtor P", "cpf_cnpj": "15151515151"},
            {"name": "Produtor Q", "cpf_cnpj": "16161616161"},
            {"name": "Produtor R", "cpf_cnpj": "17171717171"},
            {"name": "Produtor S", "cpf_cnpj": "18181818181"},
            {"name": "Produtor T", "cpf_cnpj": "19191919191"},
        ]

        producers = []
        for p in producers_data:
            producer, created = Producer.objects.update_or_create(
                cpf_cnpj=p["cpf_cnpj"],
                defaults={"name": p["name"]}
            )
            producers.append(producer)

        # Fazendas variadas para os primeiros produtores
        farms_data = [
            {"producer": producers[0], "name": "Fazenda Boa Vista", "city": "Uberlândia", "state": "MG", "total_area": 1500, "arable_area": 1000, "vegetation_area": 500},
            {"producer": producers[1], "name": "Fazenda Santa Helena", "city": "Dourados", "state": "MS", "total_area": 2300, "arable_area": 1800, "vegetation_area": 500},
            {"producer": producers[2], "name": "Fazenda Três Lagos", "city": "Maringá", "state": "PR", "total_area": 1200, "arable_area": 900, "vegetation_area": 300},
            {"producer": producers[3], "name": "Fazenda Horizonte", "city": "Campo Grande", "state": "MS", "total_area": 2000, "arable_area": 1500, "vegetation_area": 500},
            {"producer": producers[4], "name": "Fazenda Vale Verde", "city": "Ribeirão Preto", "state": "SP", "total_area": 1800, "arable_area": 1300, "vegetation_area": 500},
        ]

        farms = []
        for f in farms_data:
            farm, created = Farm.objects.update_or_create(
                producer=f["producer"],
                name=f["name"],
                defaults={
                    "city": f["city"],
                    "state": f["state"],
                    "total_area": f["total_area"],
                    "arable_area": f["arable_area"],
                    "vegetation_area": f["vegetation_area"],
                }
            )
            farms.append(farm)

        # Colheitas
        harvests_data = [
            {"name": "Safra Primavera", "year": 2023},
            {"name": "Safra Verão", "year": 2024},
            {"name": "Safra Outono", "year": 2023},
            {"name": "Safra Inverno", "year": 2024},
        ]

        harvests = []
        for h in harvests_data:
            harvest, created = Harvest.objects.update_or_create(
                name=h["name"], year=h["year"]
            )
            harvests.append(harvest)

        # Culturas diversas nas fazendas para as colheitas
        crops_data = [
            {"farm": farms[0], "harvest": harvests[0], "name": "Soja"},
            {"farm": farms[0], "harvest": harvests[1], "name": "Milho"},
            {"farm": farms[1], "harvest": harvests[0], "name": "Algodão"},
            {"farm": farms[1], "harvest": harvests[2], "name": "Feijão"},
            {"farm": farms[2], "harvest": harvests[1], "name": "Trigo"},
            {"farm": farms[3], "harvest": harvests[3], "name": "Cana-de-açúcar"},
            {"farm": farms[4], "harvest": harvests[2], "name": "Café"},
        ]

        for c in crops_data:
            Crop.objects.update_or_create(
                farm=c["farm"],
                harvest=c["harvest"],
                name=c["name"]
            )

        self.stdout.write(self.style.SUCCESS('Seeded producers, farms, harvests and crops successfully'))
