from setuptools import find_packages, setup

setup(
    name="taskflow-api",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.11",
    install_requires=[
        "fastapi==0.115.0", 
        "uvicorn==0.30.6",
        "pydantic==2.8.2",
    ],
    description="REST API para gerenciamento de tarefas com pipeline CI/CD",
    author="<Christian Salles Castilho, Rafael Areias Silveira>",
    author_email="[c.salles@gec.inatel.br], [rafael.silveira@gec.inatel.br]",
)
