-- PostgreSQL database schema setup

-- Avoid unsupported extensions on Heroku
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; -- Uncomment if supported
-- CREATE EXTENSION IF NOT EXISTS vector;      -- Uncomment if supported

-- ENUM TYPES
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'messagetypes') THEN
        CREATE TYPE public.messagetypes AS ENUM (
            'SYSTEM',
            'USER'
        );
    END IF;
END $$;

DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'moodstatus') THEN
        CREATE TYPE public.moodstatus AS ENUM (
            'VERY_POSITIVE',
            'SOMEWHAT_POSITIVE',
            'NEUTRAL',
            'SOMEWHAT_NEGATIVE',
            'VERY_NEGATIVE'
        );
    END IF;
END $$;

DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'rolestatus') THEN
        CREATE TYPE public.rolestatus AS ENUM (
            'MODERATOR',
            'USER',
            'ADMIN'
        );
    END IF;
END $$;

-- TABLES
CREATE TABLE IF NOT EXISTS public.activities (
    id uuid NOT NULL PRIMARY KEY,
    activity_type character varying(100),
    description character varying(255),
    "timestamp" timestamp without time zone,
    user_id uuid
);

CREATE TABLE IF NOT EXISTS public.alembic_version (
    version_num character varying(32) NOT NULL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS public.chat_summary (
    chat_id uuid DEFAULT public.uuid_generate_v4() NOT NULL PRIMARY KEY,
    profile_id uuid,
    summary text,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public.journals (
    journal_id uuid NOT NULL PRIMARY KEY,
    profile_id uuid,
    created_on timestamp without time zone,
    entry text,
    ai_response json
);

CREATE TABLE IF NOT EXISTS public.plans (
    plan_id uuid NOT NULL PRIMARY KEY,
    profile_id uuid,
    created_on timestamp without time zone
);

CREATE TABLE IF NOT EXISTS public.profiles (
    profile_id uuid NOT NULL PRIMARY KEY,
    user_name character varying(64) UNIQUE,
    created_on timestamp without time zone,
    updated_on timestamp without time zone,
    user_id uuid UNIQUE
);

CREATE TABLE IF NOT EXISTS public.users (
    user_id uuid NOT NULL PRIMARY KEY,
    email character varying(100) UNIQUE,
    role public.rolestatus,
    user_name character varying(64) UNIQUE,
    password_hash character varying(256),
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);

-- DROP EXISTING CONSTRAINTS (Prevent duplicates)
ALTER TABLE public.activities DROP CONSTRAINT IF EXISTS activities_user_id_fkey;
ALTER TABLE public.chat_summary DROP CONSTRAINT IF EXISTS fk_profile_id;
ALTER TABLE public.journals DROP CONSTRAINT IF EXISTS journals_profile_id_fkey;
ALTER TABLE public.plans DROP CONSTRAINT IF EXISTS plans_profile_id_fkey;
ALTER TABLE public.profiles DROP CONSTRAINT IF EXISTS profiles_user_id_fkey;

-- ADD FOREIGN KEYS
ALTER TABLE public.activities
    ADD CONSTRAINT activities_user_id_fkey
    FOREIGN KEY (user_id) REFERENCES public.users(user_id);

ALTER TABLE public.chat_summary
    ADD CONSTRAINT fk_profile_id
    FOREIGN KEY (profile_id) REFERENCES public.profiles(profile_id);

ALTER TABLE public.journals
    ADD CONSTRAINT journals_profile_id_fkey
    FOREIGN KEY (profile_id) REFERENCES public.profiles(profile_id);

ALTER TABLE public.plans
    ADD CONSTRAINT plans_profile_id_fkey
    FOREIGN KEY (profile_id) REFERENCES public.profiles(profile_id);

ALTER TABLE public.profiles
    ADD CONSTRAINT profiles_user_id_fkey
    FOREIGN KEY (user_id) REFERENCES public.users(user_id);
