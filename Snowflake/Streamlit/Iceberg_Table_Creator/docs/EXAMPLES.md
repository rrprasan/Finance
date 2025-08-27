# 🎯 Usage Examples

Real-world examples of using the Iceberg Table Creator for different use cases.

## 📈 Financial Data Pipeline

### **Scenario**: Stock market data analysis
**Goal**: Create tables for OHLCV (Open, High, Low, Close, Volume) data

### **Setup**:
1. Use **Stock Data Template**
2. Configure for daily stock data
3. Set up automated data ingestion

### **Table Schema**:
```sql
CREATE ICEBERG TABLE stock_prices (
    TICKER VARCHAR,
    TRADE_DATE DATE,
    OPEN_PRICE DOUBLE,
    HIGH_PRICE DOUBLE,
    LOW_PRICE DOUBLE,
    CLOSE_PRICE DOUBLE,
    VOLUME BIGINT
)
```

### **Sample Workflow**:
```python
# After table creation, you can insert real data:
INSERT INTO stock_prices VALUES
('AAPL', '2024-01-15', 185.50, 187.20, 184.80, 186.95, 52840000),
('MSFT', '2024-01-15', 395.20, 398.10, 394.50, 397.58, 28450000),
('GOOGL', '2024-01-15', 152.30, 153.80, 151.90, 153.45, 31250000);
```

### **Benefits**:
- ✅ Automatic partitioning by date
- ✅ Columnar storage for analytics
- ✅ Time travel capabilities
- ✅ Schema evolution support

---

## 👥 User Management System

### **Scenario**: SaaS application user data
**Goal**: Track user registrations, activity, and metadata

### **Setup**:
1. Use **User Data Template** as base
2. Add custom fields for your business
3. Enable real-time user tracking

### **Enhanced Schema**:
```sql
CREATE ICEBERG TABLE users_enhanced (
    USER_ID INTEGER,
    USERNAME VARCHAR,
    EMAIL VARCHAR,
    CREATED_DATE TIMESTAMP,
    IS_ACTIVE BOOLEAN,
    SUBSCRIPTION_TIER VARCHAR,
    LAST_LOGIN TIMESTAMP,
    TOTAL_SESSIONS INTEGER
)
```

### **Use Cases**:
- **User Analytics**: Track engagement patterns
- **Subscription Management**: Monitor tier changes
- **Compliance**: Maintain audit trails
- **Personalization**: Store user preferences

---

## 🛒 E-commerce Analytics

### **Scenario**: Online retail order processing
**Goal**: Analyze sales patterns, inventory, and customer behavior

### **Setup**:
1. Start with **Sales Data Template**
2. Add product and customer dimensions
3. Include inventory tracking

### **Multi-Table Setup**:

#### **Orders Table**:
```sql
CREATE ICEBERG TABLE orders (
    ORDER_ID INTEGER,
    CUSTOMER_ID INTEGER,
    ORDER_DATE DATE,
    ORDER_STATUS VARCHAR,
    TOTAL_AMOUNT DECIMAL(10,2),
    SHIPPING_ADDRESS VARCHAR,
    PAYMENT_METHOD VARCHAR
)
```

#### **Order Items Table**:
```sql
CREATE ICEBERG TABLE order_items (
    ORDER_ID INTEGER,
    PRODUCT_ID INTEGER,
    PRODUCT_NAME VARCHAR,
    QUANTITY INTEGER,
    UNIT_PRICE DECIMAL(10,2),
    DISCOUNT_AMOUNT DECIMAL(10,2),
    LINE_TOTAL DECIMAL(10,2)
)
```

### **Analytics Queries**:
```sql
-- Daily sales summary
SELECT 
    ORDER_DATE,
    COUNT(*) as order_count,
    SUM(TOTAL_AMOUNT) as daily_revenue
FROM orders 
WHERE ORDER_DATE >= '2024-01-01'
GROUP BY ORDER_DATE
ORDER BY ORDER_DATE;

-- Top selling products
SELECT 
    PRODUCT_NAME,
    SUM(QUANTITY) as units_sold,
    SUM(LINE_TOTAL) as revenue
FROM order_items 
GROUP BY PRODUCT_NAME
ORDER BY revenue DESC
LIMIT 10;
```

---

## 🏥 Healthcare Data Management

### **Scenario**: Patient records and medical device data
**Goal**: Secure, compliant healthcare data storage

### **Custom Schema**:
```sql
CREATE ICEBERG TABLE patient_vitals (
    PATIENT_ID VARCHAR,        -- Encrypted/hashed ID
    MEASUREMENT_DATE TIMESTAMP,
    VITAL_TYPE VARCHAR,        -- 'heart_rate', 'blood_pressure', etc.
    VALUE_NUMERIC DOUBLE,
    VALUE_TEXT VARCHAR,
    DEVICE_ID VARCHAR,
    PROVIDER_ID VARCHAR,
    NOTES VARCHAR
)
```

### **Compliance Features**:
- **Data Encryption**: Column-level encryption
- **Audit Trails**: Track all data access
- **Data Retention**: Automatic archival policies
- **Privacy**: Easy data deletion for GDPR compliance

---

## 🌐 IoT Sensor Data

### **Scenario**: Industrial IoT monitoring
**Goal**: Real-time sensor data collection and analysis

### **Time-Series Schema**:
```sql
CREATE ICEBERG TABLE sensor_readings (
    SENSOR_ID VARCHAR,
    TIMESTAMP TIMESTAMP,
    LOCATION VARCHAR,
    SENSOR_TYPE VARCHAR,
    TEMPERATURE DOUBLE,
    HUMIDITY DOUBLE,
    PRESSURE DOUBLE,
    BATTERY_LEVEL INTEGER,
    STATUS VARCHAR
)
```

### **Streaming Ingestion**:
```python
# Example Kafka consumer setup
from kafka import KafkaConsumer
import snowflake.connector

consumer = KafkaConsumer('iot-sensors')
conn = snowflake.connector.connect(...)

for message in consumer:
    sensor_data = json.loads(message.value)
    # Insert into Iceberg table
    cursor.execute("""
        INSERT INTO sensor_readings VALUES (
            %(sensor_id)s, %(timestamp)s, %(location)s,
            %(sensor_type)s, %(temperature)s, %(humidity)s,
            %(pressure)s, %(battery_level)s, %(status)s
        )
    """, sensor_data)
```

---

## 📊 Marketing Campaign Analytics

### **Scenario**: Digital marketing performance tracking
**Goal**: Measure campaign effectiveness across channels

### **Campaign Schema**:
```sql
CREATE ICEBERG TABLE campaign_events (
    EVENT_ID VARCHAR,
    CAMPAIGN_ID VARCHAR,
    USER_ID VARCHAR,
    EVENT_TYPE VARCHAR,      -- 'impression', 'click', 'conversion'
    EVENT_TIMESTAMP TIMESTAMP,
    CHANNEL VARCHAR,         -- 'google', 'facebook', 'email'
    COST_USD DECIMAL(10,4),
    REVENUE_USD DECIMAL(10,2),
    DEVICE_TYPE VARCHAR,
    LOCATION VARCHAR
)
```

### **Attribution Analysis**:
```sql
-- Multi-touch attribution
WITH user_journey AS (
    SELECT 
        USER_ID,
        CAMPAIGN_ID,
        CHANNEL,
        EVENT_TIMESTAMP,
        REVENUE_USD,
        ROW_NUMBER() OVER (
            PARTITION BY USER_ID 
            ORDER BY EVENT_TIMESTAMP
        ) as touch_sequence
    FROM campaign_events 
    WHERE EVENT_TYPE = 'conversion'
)
SELECT 
    CHANNEL,
    COUNT(*) as conversions,
    SUM(REVENUE_USD) as total_revenue,
    AVG(touch_sequence) as avg_touches_to_convert
FROM user_journey 
GROUP BY CHANNEL;
```

---

## 🎮 Gaming Analytics

### **Scenario**: Mobile game player behavior
**Goal**: Optimize game mechanics and monetization

### **Player Events Schema**:
```sql
CREATE ICEBERG TABLE player_events (
    PLAYER_ID VARCHAR,
    SESSION_ID VARCHAR,
    EVENT_TIMESTAMP TIMESTAMP,
    EVENT_TYPE VARCHAR,      -- 'level_start', 'purchase', 'achievement'
    LEVEL INTEGER,
    COINS_EARNED INTEGER,
    COINS_SPENT INTEGER,
    ITEM_ID VARCHAR,
    PURCHASE_AMOUNT DECIMAL(10,2),
    PLATFORM VARCHAR,        -- 'ios', 'android', 'web'
    GAME_VERSION VARCHAR
)
```

### **Player Segmentation**:
```sql
-- Identify whale players (high spenders)
SELECT 
    PLAYER_ID,
    COUNT(*) as total_sessions,
    SUM(COINS_SPENT) as total_coins_spent,
    SUM(PURCHASE_AMOUNT) as total_spent_usd,
    MAX(LEVEL) as highest_level
FROM player_events 
WHERE EVENT_TIMESTAMP >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY PLAYER_ID
HAVING total_spent_usd > 100
ORDER BY total_spent_usd DESC;
```

---

## 🌍 Environmental Monitoring

### **Scenario**: Climate and air quality tracking
**Goal**: Environmental data collection and trend analysis

### **Environmental Schema**:
```sql
CREATE ICEBERG TABLE environmental_data (
    STATION_ID VARCHAR,
    MEASUREMENT_TIME TIMESTAMP,
    LATITUDE DOUBLE,
    LONGITUDE DOUBLE,
    TEMPERATURE_C DOUBLE,
    HUMIDITY_PERCENT DOUBLE,
    AIR_PRESSURE_HPA DOUBLE,
    PM25_UG_M3 DOUBLE,
    PM10_UG_M3 DOUBLE,
    CO2_PPM DOUBLE,
    WIND_SPEED_MPS DOUBLE,
    WIND_DIRECTION_DEG INTEGER,
    PRECIPITATION_MM DOUBLE
)
```

### **Climate Analysis**:
```sql
-- Monthly temperature trends
SELECT 
    DATE_TRUNC('month', MEASUREMENT_TIME) as month,
    AVG(TEMPERATURE_C) as avg_temp,
    MIN(TEMPERATURE_C) as min_temp,
    MAX(TEMPERATURE_C) as max_temp,
    STDDEV(TEMPERATURE_C) as temp_variance
FROM environmental_data 
WHERE MEASUREMENT_TIME >= '2023-01-01'
GROUP BY month
ORDER BY month;

-- Air quality alerts
SELECT 
    STATION_ID,
    MEASUREMENT_TIME,
    PM25_UG_M3,
    PM10_UG_M3,
    CASE 
        WHEN PM25_UG_M3 > 55 THEN 'Unhealthy'
        WHEN PM25_UG_M3 > 35 THEN 'Moderate'
        ELSE 'Good'
    END as air_quality_status
FROM environmental_data 
WHERE PM25_UG_M3 > 35
ORDER BY PM25_UG_M3 DESC;
```

---

## 🚀 Best Practices

### **Table Design**:
1. **Partition Strategy**: Use date/time columns for partitioning
2. **Column Order**: Put frequently filtered columns first
3. **Data Types**: Choose appropriate precision for numerics
4. **Naming**: Use consistent, descriptive naming conventions

### **Performance Optimization**:
1. **Clustering**: Cluster on frequently filtered columns
2. **Compaction**: Regular table maintenance
3. **Pruning**: Leverage Iceberg's metadata pruning
4. **Batch Size**: Optimize insert batch sizes

### **Data Management**:
1. **Schema Evolution**: Plan for future schema changes
2. **Time Travel**: Leverage historical data capabilities
3. **Snapshots**: Use snapshots for data recovery
4. **Retention**: Set appropriate data retention policies

---

## 📚 Advanced Patterns

### **Slowly Changing Dimensions (SCD)**:
```sql
-- Type 2 SCD for customer data
CREATE ICEBERG TABLE customers_scd (
    CUSTOMER_ID INTEGER,
    CUSTOMER_NAME VARCHAR,
    EMAIL VARCHAR,
    PHONE VARCHAR,
    ADDRESS VARCHAR,
    VALID_FROM TIMESTAMP,
    VALID_TO TIMESTAMP,
    IS_CURRENT BOOLEAN,
    RECORD_HASH VARCHAR  -- For change detection
)
```

### **Event Sourcing**:
```sql
-- Event store pattern
CREATE ICEBERG TABLE event_store (
    EVENT_ID VARCHAR,
    AGGREGATE_ID VARCHAR,
    EVENT_TYPE VARCHAR,
    EVENT_VERSION INTEGER,
    EVENT_DATA VARIANT,  -- JSON data
    EVENT_TIMESTAMP TIMESTAMP,
    CORRELATION_ID VARCHAR
)
```

### **Data Lake Architecture**:
```
Raw Data (Bronze) → Cleaned Data (Silver) → Analytics (Gold)
     ↓                      ↓                     ↓
Iceberg Tables      Iceberg Tables        Iceberg Tables
```

---

**Ready to implement these patterns?** Start with the templates and customize them for your specific use case! 🚀
