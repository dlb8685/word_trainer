import hashlib
from django.core.cache import cache

# My hack --> don't cache results when testing. Prod requests will then hit same utils which could be cached with test data. 
    # http://stackoverflow.com/questions/6957016/detect-django-testing-mode
    # DBryan 2015-12-29
import sys
TEST = False
try:
    TEST = 'test' in sys.argv
except:
    pass


def cache_util(timeout=300):
    """
    Tries to get the output of the function from the cache firsts. Otherwise, 
    computes the function and stores the result in the cache.

    You can also pass the timeout in seconds for the cached value. By default, 
    this is 5 minutes.

    Example usage, which holds the value of expensive_function in the cache for
    10 minutes:

        @try_cache_first(timeout=600)
        def expensive_function():
            <do expensive stuff>
            return result

    All results are indexed by a hash of the function name and parameters,
    so changes to function inputs should refresh the cache automatically.
    """
    def decorator(func):

        def wrapper(*args, **kwargs):
            # Skip everything involving cache update if running in test (DBryan hack)
            if TEST == False:
                # Everything within this block is original code, skips if testing. Don't use cache in testing.
                # Build keys from function name and arguments
                caching_keys = [func.__name__]

                if args is not None: 
                    caching_keys.extend(args)

                if kwargs is not None:
                    caching_keys.extend(sorted(kwargs.items()))
                    # have to sort the caching keys because kwargs can be in random
                    # order which screws with hashing the inputs.

                # Convert the keys to a big string and hash it
                caching_keys = map(str, caching_keys)
                cache_key = '_'.join(caching_keys)
                cache_key = cache_key.encode('utf-8')
                cache_key = hashlib.sha512(cache_key).hexdigest()

                cache_key = cache_key[:250]  # max size of caching keys in memcached

                # Fetch from cache
                output = cache.get(cache_key)
            else:
                # If in testing, runs here. Forces cache_util to run function and ignore cache (DBryan)
                output = None
                
            if output is None:
                output = func(*args, **kwargs)
                if TEST == False:
                    # My addition (DBryan), only set cache if not testing
                    cache.set(cache_key, output, timeout)
            return output

        return wrapper

    return decorator