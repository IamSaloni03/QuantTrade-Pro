from django.apps import AppConfig

class DataPipelineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.apps.data_pipeline'
    label = 'quant_data_pipeline'
