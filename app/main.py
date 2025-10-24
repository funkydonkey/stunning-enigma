"""
FastAPI server for Excel Formula Optimizer.

Provides endpoints for beautifying and optimizing Excel formulas using AI.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

from app.beautifier import beautify_formula
from app.ai_agent import optimize_formula
from app.utils import validate_formula, sanitize_formula


# Pydantic models for request/response validation
class FormulaRequest(BaseModel):
    """Request model for formula input."""
    formula: str = Field(..., min_length=1, description="Excel formula to process")


class FormatResponse(BaseModel):
    """Response model for /format endpoint."""
    pretty: str = Field(..., description="Beautified formula")


class SimplifyResponse(BaseModel):
    """Response model for /simplify endpoint."""
    pretty: str = Field(..., description="Beautified formula")
    simplified: str = Field(..., description="AI-optimized formula")
    comment: str = Field(..., description="Explanation of optimizations")


# Create FastAPI app
app = FastAPI(
    title="Excel Formula Optimizer",
    description="AI-powered Excel formula beautifier and optimizer using Claude",
    version="0.1.0",
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Excel Formula Optimizer API",
        "version": "0.1.0",
        "endpoints": {
            "/format": "POST - Beautify an Excel formula",
            "/simplify": "POST - Beautify and optimize an Excel formula with AI",
            "/docs": "GET - API documentation",
        }
    }


@app.post("/format", response_model=FormatResponse)
async def format_formula(request: FormulaRequest):
    """
    Beautify an Excel formula with proper formatting and indentation.

    Args:
        request: Formula request containing the formula to beautify

    Returns:
        FormatResponse with the beautified formula

    Raises:
        HTTPException: If the formula is invalid
    """
    # Sanitize input
    formula = sanitize_formula(request.formula)

    # Validate formula
    is_valid, error_msg = validate_formula(formula)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    try:
        # Beautify the formula
        pretty = beautify_formula(formula)

        return FormatResponse(pretty=pretty)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error formatting formula: {str(e)}"
        )


@app.post("/simplify", response_model=SimplifyResponse)
async def simplify_formula(request: FormulaRequest):
    """
    Beautify and optimize an Excel formula using AI.

    This endpoint:
    1. Beautifies the formula with proper formatting
    2. Uses Claude AI to suggest an optimized/simplified version
    3. Provides an explanation of the improvements

    Args:
        request: Formula request containing the formula to optimize

    Returns:
        SimplifyResponse with beautified, optimized formulas and explanation

    Raises:
        HTTPException: If the formula is invalid or processing fails
    """
    # Sanitize input
    formula = sanitize_formula(request.formula)

    # Validate formula
    is_valid, error_msg = validate_formula(formula)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)

    try:
        # Beautify the formula
        pretty = beautify_formula(formula)

        # Optimize with AI
        optimization_result = optimize_formula(formula, pretty)

        return SimplifyResponse(
            pretty=pretty,
            simplified=optimization_result["simplified"],
            comment=optimization_result["comment"]
        )

    except ValueError as e:
        # API key or configuration error
        raise HTTPException(
            status_code=500,
            detail=f"Configuration error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error optimizing formula: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
