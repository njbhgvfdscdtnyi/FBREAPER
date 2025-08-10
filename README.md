# Facebook OSINT Dashboard - Full Stack Application

A comprehensive OSINT (Open Source Intelligence) dashboard for Facebook data collection and analysis, built with React frontend, Java Spring Boot backend, and Python scraper microservice.

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  Java Backend   │    │ Python Scraper  │
│   (Port 3000)   │◄──►│   (Port 8080)   │◄──►│   (Port 5000)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Tailwind CSS  │    │   Neo4j Database│    │   Kafka Broker  │
│   Styling       │    │   (Port 7687)   │    │   (Port 9092)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Java 17+**
- **Node.js 18+**
- **Python 3.8+**
- **Docker** (for Neo4j and Kafka)
- **Maven**

### 1. Start Infrastructure Services

```bash
# Start Neo4j and Kafka using Docker Compose
docker-compose up -d neo4j kafka
```

### 2. Start the Java Backend

```bash
cd backend-java
mvn spring-boot:run
```

The backend will be available at `http://localhost:8080`

### 3. Start the Python Scraper

```bash
cd python_scraper
pip install -r requirements.txt
python main.py
```

### 4. Start the React Frontend

```bash
cd facebook-osint-dashboard
npm install
npm start
```

The frontend will be available at `http://localhost:3000`

## 📁 Project Structure

```
├── facebook-osint-dashboard/     # React Frontend
│   ├── src/
│   │   ├── components/          # UI Components
│   │   ├── pages/              # Page Components
│   │   ├── services/           # API Services
│   │   └── types/              # TypeScript Types
│   └── package.json
│
├── backend-java/                # Spring Boot Backend
│   ├── src/main/java/com/fbreaperv1/
│   │   ├── controller/         # REST Controllers
│   │   ├── service/           # Business Logic
│   │   ├── model/             # Data Models
│   │   ├── repository/        # Data Access
│   │   ├── kafka/             # Kafka Integration
│   │   └── config/            # Configuration
│   └── pom.xml
│
└── python_scraper/             # Python Scraper Microservice
    ├── scraper/               # Scraping Logic
    ├── nlp/                   # NLP Processing
    ├── kafka_client/          # Kafka Integration
    └── main.py               # Main Entry Point
```

## 🔧 Configuration

### Backend Configuration (`backend-java/src/main/resources/application.properties`)

```properties
# Server
server.port=8080

# Neo4j
spring.neo4j.uri=bolt://localhost:7687
spring.neo4j.authentication.username=neo4j
spring.neo4j.authentication.password=neo4jpassword

# Kafka
spring.kafka.bootstrap-servers=localhost:9092
spring.kafka.consumer.group-id=fbreaper-group

# CORS
spring.web.cors.allowed-origins=http://localhost:3000
```

### Frontend Configuration

Create `.env` file in `facebook-osint-dashboard/`:

```env
REACT_APP_API_BASE_URL=http://localhost:8080/api
```

### Python Scraper Configuration

Create `.env` file in `python_scraper/`:

```env
KAFKA_BROKER=localhost:9092
KAFKA_SCRAPE_TOPIC=fbreaper-topic
KAFKA_COMMANDS_TOPIC=scraper-control
LIBRETRANSLATE_URL=http://localhost:5001/translate
```

## 🎯 Features

### Frontend Features
- **Real-time Dashboard** with live statistics
- **Search Interface** for keyword-based scraping
- **Data Visualization** with network graphs
- **Scraper Status Monitoring**
- **Responsive Design** with Tailwind CSS

### Backend Features
- **RESTful API** for frontend communication
- **Kafka Integration** for real-time data streaming
- **Neo4j Database** for graph data storage
- **Data Processing** and enrichment
- **Network Analysis** capabilities

### Python Scraper Features
- **Facebook Data Scraping** using Playwright
- **NLP Processing** for sentiment analysis
- **Kafka Integration** for data streaming
- **Async Processing** for high performance

## 🔌 API Endpoints

### Scraper Endpoints
- `POST /api/scraper/start` - Start scraper
- `POST /api/scraper/scrapeByKeyword?keyword={keyword}` - Scrape by keyword
- `GET /api/scraper/status` - Get scraper status

### Data Endpoints
- `GET /api/data/posts` - Get all posts (paginated)
- `GET /api/data/posts/search?keyword={keyword}` - Search posts by keyword
- `GET /api/data/posts/{postId}/comments` - Get comments for a post
- `GET /api/data/stats` - Get dashboard statistics

### Network Analysis Endpoints
- `GET /api/network/graph` - Get network graph data
- `GET /api/network/link-analysis?url={url}` - Analyze links

## 🐳 Docker Setup

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  neo4j:
    image: neo4j:5.15
    ports:
      - "7687:7687"
      - "7474:7474"
    environment:
      NEO4J_AUTH: neo4j/neo4jpassword
    volumes:
      - neo4j_data:/data

  kafka:
    image: confluentinc/cp-kafka:7.4.0
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092,PLAINTEXT_HOST://localhost:29092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1

  zookeeper:
    image: confluentinc/cp-zookeeper:7.4.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

volumes:
  neo4j_data:
```

## 🚨 Troubleshooting

### Common Issues

1. **Kafka Connection Issues**
   - Ensure Kafka is running: `docker ps | grep kafka`
   - Check Kafka logs: `docker logs <kafka-container-id>`

2. **Neo4j Connection Issues**
   - Verify Neo4j is accessible at `http://localhost:7474`
   - Check credentials in `application.properties`

3. **Frontend API Errors**
   - Verify backend is running on port 8080
   - Check CORS configuration
   - Ensure `.env` file is properly configured

4. **Python Scraper Issues**
   - Install dependencies: `pip install -r requirements.txt`
   - Check Kafka broker connectivity
   - Verify Facebook session setup

### Logs

- **Backend**: Check console output or `logs/` directory
- **Frontend**: Check browser console (F12)
- **Python Scraper**: Check console output for detailed logs

## 🔒 Security Considerations

- **Facebook Authentication**: Ensure proper session management
- **Rate Limiting**: Implement appropriate delays in scraping
- **Data Privacy**: Follow Facebook's terms of service
- **API Security**: Implement proper authentication for production

## 📈 Performance Optimization

- **Database Indexing**: Add indexes for frequently queried fields
- **Caching**: Implement Redis for frequently accessed data
- **Async Processing**: Use background jobs for heavy operations
- **Load Balancing**: Scale horizontally for high traffic

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is for educational and research purposes only. Please ensure compliance with Facebook's terms of service and applicable laws.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review logs for error messages
3. Create an issue with detailed information
4. Include system information and error logs