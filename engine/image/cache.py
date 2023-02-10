import pygame


class ImageCacher:
    _cache: dict[str, pygame.surface.Surface] = {}

    @classmethod
    def __call__(cls, func):
        def wrapper(*args, **kwargs):
            key: str = args[0]
            if result := cls._cache.get(key):
                return result
            result = func(*args, **kwargs)
            cls._cache[key] = result
            return result

        return wrapper

    @classmethod
    def delete_cache(cls, key: str):
        del cls._cache[key]
