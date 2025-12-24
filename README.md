# NewsMania - Backend API

A high-performance news aggregation and AI-powered content analysis platform built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- **User Authentication**: JWT-based authentication system
- **News Management**: CRUD operations for news articles
- **Categories**: Organize news into categories
- **Favorites**: Users can save favorite news articles
- **AI Integration**: AI-powered summarization and Q&A for news articles
- **Search**: Full-text search across news articles
- **Pagination**: Efficient data retrieval with pagination
- **Rate Limiting**: API rate limiting for security
- **OpenAPI Documentation**: Interactive API documentation

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **AI**: OpenAI integration for text processing
- **Caching**: Redis (optional)
- **Background Tasks**: Celery with Redis
- **Testing**: Pytest
- **Containerization**: Docker

## Project Structure

```
newsmania/
├── .env                     # Environment variables
├── .gitignore
├── requirements.txt         # Python dependencies
├── README.md
├── alembic/                 # Database migrations
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── core/                # Core functionality
│   │   ├── config.py        # Application configuration
│   │   └── security.py      # Authentication and security
│   ├── db/                  # Database related code
│   │   ├── base.py          # Database setup
│   │   └── base_crud.py     # Base CRUD operations
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   ├── news.py
│   │   ├── category.py
│   │   └── favorite.py
│   ├── schemas/             # Pydantic models
│   │   ├── user.py
│   │   ├── news.py
│   │   ├── category.py
│   │   ├── favorite.py
│   │   ├── ai.py
│   │   └── base.py
│   ├── services/            # Business logic
│   │   ├── user_service.py
│   │   ├── news_service.py
│   │   ├── category_service.py
│   │   └── ai_service.py
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependencies
│   │   └── v1/              # API version 1
│   │       ├── __init__.py
│   │       ├── api.py
│   │       └── endpoints/
│   │           ├── auth.py
│   │           ├── users.py
│   │           ├── news.py
│   │           └── categories.py
│   └── tests/               # Tests
│       ├── conftest.py
│       └── test_*.py
└── tests/                   # Integration tests
    ├── conftest.py
    └── test_*.py
```

## Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Redis (optional, for caching)
- OpenAI API key (for AI features)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/newsmania.git
   cd newsmania
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with the following variables:
   ```env
   # Database
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/newsmania
   
   # JWT
   SECRET_KEY=your-secret-key-here
   ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours
   
   # OpenAI
   OPENAI_API_KEY=your-openai-api-key
   
   # Redis (optional)
   REDIS_URL=redis://localhost:6379/0
   ```

5. Set up the database:
   ```bash
   # Run migrations
   alembic upgrade head
   
   # Or create the database manually
   createdb newsmania
   ```

6. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

7. Access the API documentation at:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token
- `GET /api/v1/auth/me` - Get current user details

### Users

- `GET /api/v1/users/` - List all users (admin only)
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/me` - Update current user
- `DELETE /api/v1/users/me` - Delete current user

### News

- `GET /api/v1/news/` - List all news articles
- `POST /api/v1/news/` - Create a new article
- `GET /api/v1/news/{news_id}` - Get article by ID
- `PUT /api/v1/news/{news_id}` - Update article
- `DELETE /api/v1/news/{news_id}` - Delete article
- `GET /api/v1/news/search` - Search articles
- `GET /api/v1/news/trending` - Get trending articles

### Categories

- `GET /api/v1/categories/` - List all categories
- `POST /api/v1/categories/` - Create a new category
- `GET /api/v1/categories/{category_id}` - Get category by ID
- `GET /api/v1/categories/{category_id}/news` - Get news by category

### Favorites

- `GET /api/v1/favorites/` - Get user's favorite articles
- `POST /api/v1/favorites/{news_id}` - Add article to favorites
- `DELETE /api/v1/favorites/{news_id}` - Remove article from favorites

### AI Features

- `POST /api/v1/ai/summary` - Generate article summary
- `POST /api/v1/ai/ask` - Ask a question about an article

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection URL | `postgresql+asyncpg://user:password@localhost:5432/newsmania` |
| `SECRET_KEY` | JWT secret key | - |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration time in minutes | `1440` |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |
| `DEBUG` | Enable debug mode | `False` |

## Database Models

### User
- id: Integer (PK)
- email: String (unique)
- name: String
- hashed_password: String
- is_active: Boolean
- is_superuser: Boolean
- created_at: DateTime
- updated_at: DateTime

### News
- id: Integer (PK)
- title: String
- content: Text
- summary: Text (nullable)
- image_url: String (nullable)
- author_id: Integer (FK to User)
- is_published: Boolean
- created_at: DateTime
- updated_at: DateTime

### Category
- id: Integer (PK)
- name: String (unique)
- description: Text (nullable)
- created_at: DateTime

### Favorite
- id: Integer (PK)
- user_id: Integer (FK to User)
- news_id: Integer (FK to News)
- created_at: DateTime

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
black .
isort .
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description of changes"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

## Deployment

### Docker

### Production

For production deployment, consider using:
- Gunicorn with Uvicorn workers
- Nginx as a reverse proxy
- HTTPS with Let's Encrypt
- Monitoring with Prometheus and Grafana
- Logging with ELK Stack or similar

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- FastAPI for the awesome web framework
- SQLAlchemy for the ORM
- OpenAI for the AI capabilities
- All the open-source libraries used in this project
