# Use Python 3.11 as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependency file
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project (including the notebook)
COPY . .

# Execute the notebook in place (runs all code cells)
CMD ["jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", "prompts_level.ipynb"]