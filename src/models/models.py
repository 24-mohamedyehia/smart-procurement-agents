from pydantic import BaseModel, Field
from typing import List

# first model 
class SuggestedSearchQueries(BaseModel):
    queries: List[str] = Field(
        ...,
        title="Suggested search queries to be passed to the search engine",
        min_items=1
    )


# second model
class SingleSearchResult(BaseModel):
    title: str
    url: str = Field(..., title="The URL of the product page")
    content: str
    score: float
    search_query: str = Field(..., title="The search query used to get this result")    

class AllSearchResults(BaseModel):
    results: List[SingleSearchResult]


# third model
class ProductSpec(BaseModel):
    specification_name: str
    specification_value: str

class SingleExtractedProduct(BaseModel):
    page_url: str = Field(..., title="The original url of the product page")
    product_title: str = Field(..., title="The title of the product")
    product_image_url: str = Field(..., title="The url of the product image")
    product_url: str = Field(..., title="The url of the product")
    product_current_price: float = Field(..., title="The current price of the product")
    product_original_price: float = Field(
        default=None,
        title="The original price of the product before discount. Set to None if no discount"
    )
    product_discount_percentage: float = Field(
        default=None,
        title="The discount percentage of the product. Set to None if no discount"
    )
    product_specs: List[ProductSpec] = Field(
        ...,
        title="The specifications of the product. Focus on the most important specs to compare.",
        min_items=1,
        max_items=5
    )
    agent_recommendation_rank: int = Field(
        ...,
        title="The rank of the product to be considered in the final procurement report. (out of 5, Higher is Better)"
    )
    agent_recommendation_notes: List[str] = Field(
        ...,
        title="A set of notes why you would recommend or not recommend this product."
    )

class AllExtractedProducts(BaseModel):
    products: List[SingleExtractedProduct]
