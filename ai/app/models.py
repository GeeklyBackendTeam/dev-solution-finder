# app/models.py

from langchain_core.pydantic_v1 import BaseModel, Field

class TechnologyComparison(BaseModel):
    DevelopedBy: str = Field(description="The company or individual who developed the technology.")
    InitialRelease: str = Field(description="The initial release date of the technology.")
    CurrentVersion: str = Field(description="The current version of the technology.")
    CurrentVersionReleaseDate: str = Field(description="The release date of the current version.")
    Type: str = Field(description="The type of technology, e.g., library or framework.")
    Language: str = Field(description="The programming language used by the technology.")
    DataBinding: str = Field(description="The type of data binding used.")
    DOM: str = Field(description="The type of DOM used.")
    ComponentBased: str = Field(description="Whether the technology is component-based.")
    LearningCurve: str = Field(description="The learning curve for the technology.")
    Performance: str = Field(description="The performance characteristics of the technology.")
    CommunitySupport: str = Field(description="The level of community support available for the technology.")
    Scalability: str = Field(description="The scalability of the technology.")
    Serverless: str = Field(description="Support for serverless architecture.")
    VirtualDOM: str = Field(description="The use of virtual DOM.")
    RenderingPattern: str = Field(description="The rendering pattern used.")

class ComparisonOutput(BaseModel):
    __root__: dict[str, TechnologyComparison]
