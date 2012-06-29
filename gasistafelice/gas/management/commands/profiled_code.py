from django.core.management.base import BaseCommand, CommandError

import hotshot.stats

ENCODING = "iso-8859-1"

class Command(BaseCommand):
    """" This command 

"""
    args = "<profiling_file_name> <rows_to_show>"
    
    help = """Shows the first n rows of the chosen profiling file."""    

    def handle(self, *args, **options):

        try:
            file_name = args[0]
            num_rows = int(args[1])
        except:
            raise CommandError("Usage profiled_code: %s" % (self.args))

        stats = hotshot.stats.load(file_name)
        #stats.strip_dirs()
        stats.sort_stats('time', 'calls')
        stats.print_stats(num_rows)
