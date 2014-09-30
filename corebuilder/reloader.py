import sys

import sublime


st_version = 2
# With the way ST3 works, the sublime module is not "available" at startup
# which results in an empty version number
if sublime.version() == '' or int(sublime.version()) > 3000:
    st_version = 3
    from imp import reload


# Python allows reloading modules on the fly, which allows us to do live upgrades.
# The only caveat to this is that you have to reload in the dependency order.
#
# Thus is module A depends on B and we don't reload B before A, when A is reloaded
# it will still have a reference to the old B. Thus we hard-code the dependency
# order of the various Package Control modules so they get reloaded properly.
#
# There are solutions for doing this all programatically, but this is much easier
# to understand.

reload_mods = []
for mod in sys.modules:
    if mod[0:11].lower() == 'corebuilder' and sys.modules[mod] != None:
        reload_mods.append(mod)

mod_prefix = 'corebuilder'
if st_version == 3:
    mod_prefix = 'CoreBuilder.' + mod_prefix

mods_load_order = [
    '',

    '.sys_path',
    '.cache',
    '.http_cache',
    '.console_write',
    '.show_error',
    '.unicode',
    '.thread_progress',
    '.business_object_io',

    '.clients',
    '.clients.client_exception',
    '.clients.json_api_client',

    '.providers',
    '.providers.provider_exception',
    '.providers.repository_provider',

    '.download_manager',
    '.download_authenticator',

    '.downloaders',
    '.downloaders.downloader_exception',
    '.downloaders.rate_limit_exception',
    '.downloaders.binary_not_found_error',
    '.downloaders.non_clean_exit_error',
    '.downloaders.non_http_error',
    '.downloaders.caching_downloader',
    '.downloaders.decoding_downloader',
    '.downloaders.limiting_downloader',
    '.downloaders.cert_provider',
    '.downloaders.urllib_downloader',
    '.downloaders.cli_downloader',
    '.downloaders.curl_downloader',
    '.downloaders.wget_downloader',
    '.downloaders.wininet_downloader',
    '.downloaders.background_downloader',

    '.business_object_manager',
    '.business_object_opener',
    '.business_object_saver',

    '.commands',
    '.commands.list_business_objects_command',
    '.commands.save_business_object_command',
    '.commands.open_business_object_command'
]

for suffix in mods_load_order:
    mod = mod_prefix + suffix
    if mod in reload_mods:
        reload(sys.modules[mod])
