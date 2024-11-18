from enum import Enum


class AIModels(Enum):
    pass


class GPTModels(AIModels):
    GPT3_TURBO = 'gpt-3.5-turbo'
    GPT4O_MINI = 'gpt-4o-mini'
    GPT4O = 'gpt-4o'
    GPT4 = 'gpt-4'
    GPT4_TURBO = 'gpt-4-turbo'


class FluxModels(AIModels):
    FLUX = 'flux'
    FLUX_PRO = 'flux-pro'
    FLUX_REALISM = 'flux-realism'
    FLUX_ANIME = 'flux-anime'
    FLUX_DISNEY = 'flux-disney'
    FLUX_3D = 'flux-3d'
    FLUX_PIXEL = 'flux-pixel'
    FLUX_4o = 'flux-4o'
