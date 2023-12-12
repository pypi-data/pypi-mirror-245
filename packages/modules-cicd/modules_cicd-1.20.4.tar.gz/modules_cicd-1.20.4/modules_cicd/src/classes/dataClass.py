from dataclasses import dataclass, field

from .TypeProjectEnum import TypeProject


@dataclass
class Repository:
    name: str = field(default="")
    new_description: str = field(default="")
    new_name_repo: str = field(default="")
    users: list[str] = field(default_factory=list)
    users_del: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    type: str = field(default="")
    branch: str = field(default="")
    is_zip: bool = field(default=False)
    nameZip: str = field(default="")
    token: str = field(default="")
    template: str = field(default=False)
    prefix_back: str = field(default="")
    prefix_front: str = field(default="")


@dataclass
class TypeProjectTemplate:
    provider: TypeProject
    name: str
    branch: str
    repo_template: str
    url: str = field(default="")
    cloneUrl: str = field(default="")
    user: str = field(default="")
    password: str = field(default="")

    def __post_init__(self):
        self.cloneUrl = self.url % (
            self.user,
            self.password,
            self.user,
            self.name,
        )