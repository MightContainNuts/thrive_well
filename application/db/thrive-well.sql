--
-- PostgreSQL database dump
--

-- Dumped from database version 17.3
-- Dumped by pg_dump version 17.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: vector; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA public;


--
-- Name: EXTENSION vector; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION vector IS 'vector data type and ivfflat and hnsw access methods';


--
-- Name: messagetypes; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.messagetypes AS ENUM (
    'SYSTEM',
    'USER'
);


--
-- Name: moodstatus; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.moodstatus AS ENUM (
    'VERY_POSITIVE',
    'SOMEWHAT_POSITIVE',
    'NEUTRAL',
    'SOMEWHAT_NEGATIVE',
    'VERY_NEGATIVE'
);


--
-- Name: rolestatus; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.rolestatus AS ENUM (
    'MODERATOR',
    'USER',
    'ADMIN'
);


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: activities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activities (
    id uuid NOT NULL,
    activity_type character varying(100),
    description character varying(255),
    "timestamp" timestamp without time zone,
    user_id uuid
);


--
-- Name: chat_summary; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.chat_summary (
    chat_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    profile_id uuid,
    summary text,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: journals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.journals (
    journal_id uuid NOT NULL,
    profile_id uuid,
    created_on timestamp without time zone,
    entry text,
    ai_response json
);


--
-- Name: medications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.medications (
    id uuid NOT NULL,
    name character varying(100),
    fda_code character varying(10),
    description character varying(255),
    side_effects public.vector(384),
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);


--
-- Name: plans; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.plans (
    plan_id uuid NOT NULL,
    profile_id uuid,
    created_on timestamp without time zone
);


--
-- Name: profiles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.profiles (
    profile_id uuid NOT NULL,
    user_name character varying(64),
    created_on timestamp without time zone,
    updated_on timestamp without time zone,
    user_id uuid,
    cancer_type character varying(100),
    medication character varying(100)
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    user_id uuid NOT NULL,
    email character varying(100),
    role public.rolestatus,
    user_name character varying(64),
    password_hash character varying(256),
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);


--
-- Name: vector_embeddings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.vector_embeddings (
    id uuid NOT NULL,
    url character varying NOT NULL,
    text text NOT NULL,
    created_on timestamp without time zone,
    updated_on timestamp without time zone,
    embedding public.vector(384),
    profile_id uuid
);


--
-- Name: activities activities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_pkey PRIMARY KEY (id);


--
-- Name: chat_summary chat_summary_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chat_summary
    ADD CONSTRAINT chat_summary_pkey PRIMARY KEY (chat_id);


--
-- Name: journals journals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.journals
    ADD CONSTRAINT journals_pkey PRIMARY KEY (journal_id);


--
-- Name: medications medications_fda_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medications
    ADD CONSTRAINT medications_fda_code_key UNIQUE (fda_code);


--
-- Name: medications medications_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medications
    ADD CONSTRAINT medications_name_key UNIQUE (name);


--
-- Name: medications medications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.medications
    ADD CONSTRAINT medications_pkey PRIMARY KEY (id);


--
-- Name: plans plans_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plans
    ADD CONSTRAINT plans_pkey PRIMARY KEY (plan_id);


--
-- Name: profiles profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_pkey PRIMARY KEY (profile_id);


--
-- Name: profiles profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_user_id_key UNIQUE (user_id);


--
-- Name: profiles profiles_user_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_user_name_key UNIQUE (user_name);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_user_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_user_name_key UNIQUE (user_name);


--
-- Name: vector_embeddings vector_embeddings_url_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vector_embeddings
    ADD CONSTRAINT vector_embeddings_url_key UNIQUE (url);


--
-- Name: activities activities_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: chat_summary fk_profile_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chat_summary
    ADD CONSTRAINT fk_profile_id FOREIGN KEY (profile_id) REFERENCES public.profiles(profile_id);


--
-- Name: journals journals_profile_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.journals
    ADD CONSTRAINT journals_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES public.profiles(profile_id);


--
-- Name: plans plans_profile_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plans
    ADD CONSTRAINT plans_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES public.profiles(profile_id);


--
-- Name: profiles profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.profiles
    ADD CONSTRAINT profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: vector_embeddings vector_embeddings_profile_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.vector_embeddings
    ADD CONSTRAINT vector_embeddings_profile_id_fkey FOREIGN KEY (profile_id) REFERENCES public.profiles(profile_id);


--
-- PostgreSQL database dump complete
--

