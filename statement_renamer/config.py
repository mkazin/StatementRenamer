""" Configuration settings """
LOCATION = 'TestData'
DESTINATION = None
QUIET = False
VERBOSE = True
SIMULATE = False
HASH_ONLY = False
EXTRACT_ONLY = False

# # @staticmethod
# def from_parser(parser):
#     """ Instantiates a Config object based on values in ArgumentParser """
#     args = parser.parse_args()
#     # location = args.location
#     # destination = args.destination
#     # quiet=args.quiet
#     # verbose=args.verbose
#     # simulate=args.simulate
#     # hash_only=args.hash_only
#     # extract_only=args.extract_only
#     config.LOCATION = args.location
#     config.DESTINATION = args.destination
#     config.QUIET = args.quiet
#     config.VERBOSE = args.verbose
#     config.SIMULATE = args.simulate
#     config.HASH_ONLY = args.hash_only
#     config.EXTRACT_ONLY = args.extract_only


# def use(configuration):
#     nonlocal CONFIG
#     CONFIG = configuration
#     # config.location = configuration.location

# class Config(object):
#     """ Data object holding the parameters of the task to execute """
#     @staticmethod
#     def __get_val_or__(obj, field, default):
#         if obj:
#             return obj.get(field)
#         return default

#     @staticmethod
#     def from_parser(parser):
#         """ Instantiates a Config object based on values in ArgumentParser """
#         args = parser.parse_args()
#         return Config(
#             location=args.location, destination=args.destination, quiet=args.quiet, verbose=args.verbose,
#             simulate=args.simulate, hash_only=args.hash_only, extract_only=args.extract_only)

#     @staticmethod
#     def test_config():
#         """ Instantiates a Config object based on values in ArgumentParser """
#         return Config(
#             location='TestData', destination='TestData', quiet=False, verbose=True,
#             simulate=False, hash_only=False, extract_only=False)

#     def __init__(self, location, destination=None,
#                  quiet=False, verbose=False, simulate=False,
#                  hash_only=False, extract_only=False):
#         self.location = location
#         self.destination = destination
#         self.quiet = quiet
#         self.verbose = verbose
#         self.simulate = simulate
#         self.hash_only = hash_only
#         self.extract_only = extract_only
