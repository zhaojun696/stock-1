from pytdx.hq import TdxHq_API
if __name__ == '__main__':
    api = TdxHq_API(raise_exception=False)
    result = api.get_security_quotes(1, '002362')
    print(result)
