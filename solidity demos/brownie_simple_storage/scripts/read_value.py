from brownie import SimpleStorage, accounts, config


def read_contract():
    simple_storage = SimpleStorage[-1]
    #index that's one less than the length
    #ABI
    #address
    print(simple_storage.retrieve())
def main():
    read_contract()