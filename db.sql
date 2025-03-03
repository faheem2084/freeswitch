CREATE TABLE fs_directory (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    ha1 VARCHAR(32) NOT NULL,  -- Store MD5 hash
    effective_caller_id_name VARCHAR(255),
    effective_caller_id_number VARCHAR(255),
    outbound_caller_id_name VARCHAR(255),
    outbound_caller_id_number VARCHAR(255),
    voicemail_enabled BOOLEAN DEFAULT TRUE,
    user_context VARCHAR(255) DEFAULT 'default',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (domain, user_id)
);

CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_timestamp
BEFORE UPDATE ON fs_directory
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();
