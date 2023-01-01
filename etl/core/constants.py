SQL_TEMPLATES = {
    'table_id': ("SELECT distinct(id), modified "
                 "FROM content.{} "
                 "WHERE modified >= %(date)s  "
                 "ORDER BY modified limit %(limit)s "
                 "OFFSET %(offset)s"),
    'person_id': ('SELECT p.id, full_name, pfw.role, pfw.film_work_id '
                  'FROM content.person p '
                  'LEFT JOIN content.person_film_work pfw on p.id = pfw.person_id '
                  'WHERE p.id IN %(persons_ids)s'),
    'genre_id': ('SELECT g.id, g.name, g.description, gfw.film_work_id '
                 'FROM content.genre g '
                 'JOIN content.genre_film_work gfw on g.id = gfw.genre_id '
                 'WHERE g.id IN %(genres_ids)s'),
    'related_film_id': ('SELECT fw.id FROM content.film_work fw '
                        'LEFT JOIN content.{}_film_work rfw ON rfw.film_work_id = fw.id '
                        'WHERE rfw.{}_id IN %(ids)s '
                        'ORDER BY fw.modified'),
    'films': ('SELECT '
              'fw.id as fw_id, '
              'fw.title, '
              'fw.description, '
              'fw.rating, '
              'fw.type, '
              'fw.created, '
              'fw.modified, '
              'pfw.role, '
              'p.id, p.full_name, '
              'g.name , g.id as genre_id '
              'FROM content.film_work fw '
              'LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id '
              'LEFT JOIN content.person p ON p.id = pfw.person_id '
              'LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id '
              'LEFT JOIN content.genre g ON g.id = gfw.genre_id '
              'WHERE fw.id IN %(films_id)s')
}

INDEX_SETTINGS = {
    'index': {
        'refresh_interval': '1s',
        'number_of_shards': '1',
        'analysis': {
            'filter': {
                'english_stop': {
                    'type': 'stop',
                    'stopwords': '_english_'
                },
                'english_stemmer': {
                    'type': 'stemmer',
                    'language': 'english'
                },
                'english_possessive_stemmer': {
                    'type': 'stemmer',
                    'language': 'possessive_english'
                },
                'russian_stop': {
                    'type': 'stop',
                    'stopwords': '_russian_'
                },
                'russian_stemmer': {
                    'type': 'stemmer',
                    'language': 'russian'
                }
            },
            'analyzer': {
                'ru_en': {
                    'tokenizer': 'standard',
                    'filter': [
                        'lowercase',
                        'english_stop',
                        'english_stemmer',
                        'english_possessive_stemmer',
                        'russian_stop',
                        'russian_stemmer'
                    ]
                }
            }
        },
        'number_of_replicas': '1',
    }
}

MOVIES_SETTINGS = {
    'index': 'movies',
    'mappings': {
        'dynamic': 'strict',
        'properties': {
            'uuid': {
                'type': 'keyword'
            },
            'imdb_rating': {
                'type': 'float'
            },
            'title': {
                'type': 'text',
                'fields': {
                    'keyword': {
                        'type': 'keyword'
                    }
                },
                'analyzer': 'ru_en'
            },
            'genre': {
                'type': 'keyword'
            },
            'description': {
                'type': 'text',
                'analyzer': 'ru_en'
            },
            'created': {
                'type': 'date'
            },
            'directors': {
                'type': 'nested',
                'dynamic': 'strict',
                'properties': {
                    'uuid': {
                        'type': 'keyword'
                    },
                    'full_name': {
                        'type': 'text',
                        'analyzer': 'ru_en'
                    }
                }
            },
            'directors_names': {
                'type': 'text',
                'analyzer': 'ru_en'
            },
            'writers': {
                'type': 'nested',
                'dynamic': 'strict',
                'properties': {
                    'uuid': {
                        'type': 'keyword'
                    },
                    'full_name': {
                        'type': 'text',
                        'analyzer': 'ru_en'
                    }
                }
            },
            'writers_names': {
                'type': 'text',
                'analyzer': 'ru_en'
            },
            'actors': {
                'type': 'nested',
                'dynamic': 'strict',
                'properties': {
                    'uuid': {
                        'type': 'keyword'
                    },
                    'full_name': {
                        'type': 'text',
                        'analyzer': 'ru_en'
                    }
                }
            },
            'actors_names': {
                'type': 'text',
                'analyzer': 'ru_en'
            }
        }
    },
    'settings': INDEX_SETTINGS
}

PERSONS_SETTINGS = {
    'index': 'persons',
    'mappings': {
        'dynamic': 'strict',
        'properties': {
            'uuid': {
                'type': 'keyword'
            },
            'full_name': {
                'type': 'text',
                'fields': {
                    'keyword': {
                        'type': 'keyword'
                    }
                },
                'analyzer': 'ru_en'
            },
            'role': {
                'type': 'keyword'
            },
            'film_ids': {
                'type': 'keyword'
            },
        }
    },
    'settings': INDEX_SETTINGS
}

GENRES_SETTINGS = {
    'index': 'genres',
    'mappings': {
        'dynamic': 'strict',
        'properties': {
            'uuid': {
                'type': 'keyword'
            },
            'name': {
                'type': 'text',
                'fields': {
                    'keyword': {
                        'type': 'keyword'
                    }
                },
                'analyzer': 'ru_en'
            },
            'description': {
                'type': 'text',
                'analyzer': 'ru_en'
            },
            'film_ids': {
                'type': 'keyword'
            },
        }
    },
    'settings': INDEX_SETTINGS
}
