from cpt.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="altairwei", archs=["x86_64"], build_policy="missing")
    builder.add_common_builds(pure_c=True)
    builder.run()