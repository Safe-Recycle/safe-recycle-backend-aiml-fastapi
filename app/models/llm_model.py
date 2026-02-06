from sqlmodel import Field, SQLModel

class LLMModel(SQLModel, table=True):
    __tablename__ = "items"

    id: int | None = Field(default=None, primary_key=True)
    model_name: str = Field(index=True)
    prompt: str = Field(index=True)
    output_message: str = Field(index=True)

