import argparse


class EZ_CLI:

    def __init__(self):
        self.command_tree = {
            'generate': {
                'scaffolding': self.__scaffolding,
                'quickstart': self.__quickstart
            }
        }
        self.parser = self.setup_parser()


    def setup_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        generate = subparsers.add_parser('generate')
        generate_subparsers = generate.add_subparsers(dest='generate')
        for subcmd in self.command_tree['generate']:
            generate_subparsers.add_parser(subcmd)
        return parser


    def __scaffolding(self):
        print('scaffolding')

    def __quickstart(self):
        print('quickstart')

    def __call__(self):
        args = self.parser.parse_args()
        subp = self.command_tree['generate'].get(args.generate)
        subp()

if __name__ == '__main__':
    cli = EZ_CLI()
    cli()



    