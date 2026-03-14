#!/bin/bash
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Starting Blog API setup...${NC}"

# ==========================================
# Step 1: Check .env variables
# ==========================================
echo -e "${YELLOW}Step 1: Checking environment variables...${NC}"

if [ ! -f ".env" ]; then
    echo -e "${RED}ERROR: .env file not found!${NC}"
    exit 1
fi

source .env

REQUIRED_VARS="SECRET_KEY BLOG_ENV_ID REDIS_HOST REDIS_PORT REDIS_DB"

for var in $REQUIRED_VARS; do
    if [ -z "${!var}" ]; then
        echo -e "${RED}ERROR: Missing required variable: $var${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✓ Environment variables OK${NC}"

# ==========================================
# Step 2: Create venv and install deps
# ==========================================
echo -e "${YELLOW}Step 2: Setting up virtual environment...${NC}"

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

source venv/bin/activate
pip install -r requirements/base.txt -q
echo -e "${GREEN}✓ Dependencies installed${NC}"

# ==========================================
# Step 3: Run migrations
# ==========================================
echo -e "${YELLOW}Step 3: Running migrations...${NC}"
cd backend
python manage.py migrate --noinput
echo -e "${GREEN}✓ Migrations done${NC}"

# ==========================================
# Step 4: Collect static files
# ==========================================
echo -e "${YELLOW}Step 4: Collecting static files...${NC}"
python manage.py collectstatic --noinput
echo -e "${GREEN}✓ Static files collected${NC}"

# ==========================================
# Step 5: Compile translations
# ==========================================
echo -e "${YELLOW}Step 5: Compiling translations...${NC}"
python manage.py compilemessages
echo -e "${GREEN}✓ Translations compiled${NC}"

# ==========================================
# Step 6: Create superuser
# ==========================================
echo -e "${YELLOW}Step 6: Creating superuser...${NC}"
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@blog.com').exists():
    User.objects.create_superuser(
        email='admin@blog.com',
        first_name='Admin',
        last_name='User',
        password='admin123',
    )
    print('Superuser created')
else:
    print('Superuser already exists')
"
echo -e "${GREEN}✓ Superuser ready${NC}"

# ==========================================
# Step 7: Seed data
# ==========================================
echo -e "${YELLOW}Step 7: Seeding test data...${NC}"
python manage.py seed_data
echo -e "${GREEN}✓ Test data seeded${NC}"

# ==========================================
# Step 8: Start server
# ==========================================
echo -e "${GREEN}"
echo "==========================================="
echo "  Blog API is ready!"
echo "==========================================="
echo "  API:      http://127.0.0.1:8000/api/"
echo "  Swagger:  http://127.0.0.1:8000/api/docs/"
echo "  ReDoc:    http://127.0.0.1:8000/api/redoc/"
echo "  Admin:    http://127.0.0.1:8000/admin/"
echo "-------------------------------------------"
echo "  Superuser: admin@blog.com / admin123"
echo "==========================================="
echo -e "${NC}"

echo -e "${YELLOW}Step 8: Starting development server...${NC}"
python manage.py runserver
