from setuptools import setup

package_name = "hb_move_turtle"

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="aa",
    maintainer_email="fresmea@naver.com",
    description="TODO: Package description",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "hbmove = hb_move_turtle.hbmove:main",
            "hbmove_turtlesim = hb_move_turtle.hbmove_turtlesim:main",
            "hbmove_sub = hb_move_turtle.hbmove_sub:main",
            "hbmove_turtlebot = hb_move_turtle.hbmove_turtlebot:main",
        ],
    },
)
