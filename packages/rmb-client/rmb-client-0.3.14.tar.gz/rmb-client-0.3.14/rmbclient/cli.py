import argparse

def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Interactive CLI for RMB client.")
    parser.add_argument('-a', '--api_url', type=str, required=True, help='The API URL for the RMB client.')
    parser.add_argument('-t', '--token', type=str, required=True, help='The token for authentication.')

    args = parser.parse_args()

    # 导入 RMB 类
    from rmbclient import RMB
    rmb = RMB(token=args.token, api_url=args.api_url)
    print("\n----- RMB 客户端初始化完成！您可以使用 'rmb' 来访问RMB的方法。-----\n")

    try:
        # 尝试导入 IPython
        from IPython import start_ipython
        start_ipython(argv=[], user_ns={'rmb': rmb})
    except ImportError:
        # 如果 IPython 未安装，使用标准 Python shell
        import code
        code.interact(local=locals())


if __name__ == "__main__":
    main()
