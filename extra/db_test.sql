--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO gf_stage;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO gf_stage;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO gf_stage;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO gf_stage;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_message; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE auth_message (
    id integer NOT NULL,
    user_id integer NOT NULL,
    message text NOT NULL
);


ALTER TABLE public.auth_message OWNER TO gf_stage;

--
-- Name: auth_message_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE auth_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_message_id_seq OWNER TO gf_stage;

--
-- Name: auth_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE auth_message_id_seq OWNED BY auth_message.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO gf_stage;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO gf_stage;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    password character varying(128) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO gf_stage;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO gf_stage;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO gf_stage;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO gf_stage;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO gf_stage;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO gf_stage;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: base_contact; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE base_contact (
    id integer NOT NULL,
    flavour character varying(32) NOT NULL,
    value character varying(256) NOT NULL,
    is_preferred boolean NOT NULL,
    description character varying(128) NOT NULL
);


ALTER TABLE public.base_contact OWNER TO gf_stage;

--
-- Name: base_contact_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE base_contact_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_contact_id_seq OWNER TO gf_stage;

--
-- Name: base_contact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE base_contact_id_seq OWNED BY base_contact.id;


--
-- Name: base_defaulttransition; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE base_defaulttransition (
    id integer NOT NULL,
    workflow_id integer NOT NULL,
    state_id integer NOT NULL,
    transition_id integer NOT NULL
);


ALTER TABLE public.base_defaulttransition OWNER TO gf_stage;

--
-- Name: base_defaulttransition_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE base_defaulttransition_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_defaulttransition_id_seq OWNER TO gf_stage;

--
-- Name: base_defaulttransition_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE base_defaulttransition_id_seq OWNED BY base_defaulttransition.id;


--
-- Name: base_historicalcontact; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE base_historicalcontact (
    id integer NOT NULL,
    flavour character varying(32) NOT NULL,
    value character varying(256) NOT NULL,
    is_preferred boolean NOT NULL,
    description character varying(128) NOT NULL,
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL
);


ALTER TABLE public.base_historicalcontact OWNER TO gf_stage;

--
-- Name: base_historicalcontact_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE base_historicalcontact_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_historicalcontact_history_id_seq OWNER TO gf_stage;

--
-- Name: base_historicalcontact_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE base_historicalcontact_history_id_seq OWNED BY base_historicalcontact.history_id;


--
-- Name: base_historicaldefaulttransition; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE base_historicaldefaulttransition (
    id integer NOT NULL,
    workflow_id integer NOT NULL,
    state_id integer NOT NULL,
    transition_id integer NOT NULL,
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL
);


ALTER TABLE public.base_historicaldefaulttransition OWNER TO gf_stage;

--
-- Name: base_historicaldefaulttransition_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE base_historicaldefaulttransition_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_historicaldefaulttransition_history_id_seq OWNER TO gf_stage;

--
-- Name: base_historicaldefaulttransition_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE base_historicaldefaulttransition_history_id_seq OWNED BY base_historicaldefaulttransition.history_id;


--
-- Name: base_historicalperson; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE base_historicalperson (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    surname character varying(128) NOT NULL,
    display_name character varying(128) NOT NULL,
    ssn character varying(128),
    user_id integer,
    address_id integer,
    avatar character varying(100),
    website character varying(200) NOT NULL,
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL
);


ALTER TABLE public.base_historicalperson OWNER TO gf_stage;

--
-- Name: base_historicalperson_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE base_historicalperson_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_historicalperson_history_id_seq OWNER TO gf_stage;

--
-- Name: base_historicalperson_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE base_historicalperson_history_id_seq OWNED BY base_historicalperson.history_id;


--
-- Name: base_historicalplace; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE base_historicalplace (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    description text NOT NULL,
    address character varying(128) NOT NULL,
    zipcode character varying(128) NOT NULL,
    city character varying(128) NOT NULL,
    province character varying(2) NOT NULL,
    lon double precision,
    lat double precision,
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL
);


ALTER TABLE public.base_historicalplace OWNER TO gf_stage;

--
-- Name: base_historicalplace_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE base_historicalplace_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_historicalplace_history_id_seq OWNER TO gf_stage;

--
-- Name: base_historicalplace_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE base_historicalplace_history_id_seq OWNED BY base_historicalplace.history_id;


--
-- Name: base_person; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE base_person (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    surname character varying(128) NOT NULL,
    display_name character varying(128) NOT NULL,
    ssn character varying(128),
    user_id integer,
    address_id integer,
    avatar character varying(100),
    website character varying(200) NOT NULL
);


ALTER TABLE public.base_person OWNER TO gf_stage;

--
-- Name: base_person_contact_set; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE base_person_contact_set (
    id integer NOT NULL,
    person_id integer NOT NULL,
    contact_id integer NOT NULL
);


ALTER TABLE public.base_person_contact_set OWNER TO gf_stage;

--
-- Name: base_person_contact_set_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE base_person_contact_set_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_person_contact_set_id_seq OWNER TO gf_stage;

--
-- Name: base_person_contact_set_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE base_person_contact_set_id_seq OWNED BY base_person_contact_set.id;


--
-- Name: base_person_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE base_person_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_person_id_seq OWNER TO gf_stage;

--
-- Name: base_person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE base_person_id_seq OWNED BY base_person.id;


--
-- Name: base_place; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE base_place (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    description text NOT NULL,
    address character varying(128) NOT NULL,
    zipcode character varying(128) NOT NULL,
    city character varying(128) NOT NULL,
    province character varying(2) NOT NULL,
    lon double precision,
    lat double precision
);


ALTER TABLE public.base_place OWNER TO gf_stage;

--
-- Name: base_place_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE base_place_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_place_id_seq OWNER TO gf_stage;

--
-- Name: base_place_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE base_place_id_seq OWNED BY base_place.id;


--
-- Name: blockconfiguration; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE blockconfiguration (
    id integer NOT NULL,
    user_id integer NOT NULL,
    blocktype character varying(255) NOT NULL,
    resource_type character varying(255) NOT NULL,
    resource_id character varying(255) NOT NULL,
    page smallint NOT NULL,
    "position" smallint NOT NULL,
    confdata text
);


ALTER TABLE public.blockconfiguration OWNER TO gf_stage;

--
-- Name: blockconfiguration_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE blockconfiguration_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.blockconfiguration_id_seq OWNER TO gf_stage;

--
-- Name: blockconfiguration_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE blockconfiguration_id_seq OWNED BY blockconfiguration.id;


--
-- Name: captcha_captchastore; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE captcha_captchastore (
    id integer NOT NULL,
    challenge character varying(32) NOT NULL,
    response character varying(32) NOT NULL,
    hashkey character varying(40) NOT NULL,
    expiration timestamp with time zone NOT NULL
);


ALTER TABLE public.captcha_captchastore OWNER TO gf_stage;

--
-- Name: captcha_captchastore_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE captcha_captchastore_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.captcha_captchastore_id_seq OWNER TO gf_stage;

--
-- Name: captcha_captchastore_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE captcha_captchastore_id_seq OWNED BY captcha_captchastore.id;


--
-- Name: des_des; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE des_des (
    site_ptr_id integer NOT NULL,
    cfg_time integer NOT NULL,
    logo character varying(100),
    CONSTRAINT des_des_cfg_time_check CHECK ((cfg_time >= 0))
);


ALTER TABLE public.des_des OWNER TO gf_stage;

--
-- Name: des_des_info_people_set; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE des_des_info_people_set (
    id integer NOT NULL,
    des_id integer NOT NULL,
    person_id integer NOT NULL
);


ALTER TABLE public.des_des_info_people_set OWNER TO gf_stage;

--
-- Name: des_des_info_people_set_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE des_des_info_people_set_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.des_des_info_people_set_id_seq OWNER TO gf_stage;

--
-- Name: des_des_info_people_set_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE des_des_info_people_set_id_seq OWNED BY des_des_info_people_set.id;


--
-- Name: des_siteattr; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE des_siteattr (
    id integer NOT NULL,
    name character varying(63) NOT NULL,
    value text NOT NULL,
    atype character varying(63) NOT NULL,
    descr character varying(255) NOT NULL
);


ALTER TABLE public.des_siteattr OWNER TO gf_stage;

--
-- Name: des_siteattr_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE des_siteattr_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.des_siteattr_id_seq OWNER TO gf_stage;

--
-- Name: des_siteattr_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE des_siteattr_id_seq OWNED BY des_siteattr.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    content_type_id integer,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO gf_stage;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO gf_stage;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_comment_flags; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE django_comment_flags (
    id integer NOT NULL,
    user_id integer NOT NULL,
    comment_id integer NOT NULL,
    flag character varying(30) NOT NULL,
    flag_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_comment_flags OWNER TO gf_stage;

--
-- Name: django_comment_flags_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE django_comment_flags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_comment_flags_id_seq OWNER TO gf_stage;

--
-- Name: django_comment_flags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE django_comment_flags_id_seq OWNED BY django_comment_flags.id;


--
-- Name: django_comments; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE django_comments (
    id integer NOT NULL,
    content_type_id integer NOT NULL,
    object_pk text NOT NULL,
    site_id integer NOT NULL,
    user_id integer,
    user_name character varying(50) NOT NULL,
    user_email character varying(75) NOT NULL,
    user_url character varying(200) NOT NULL,
    comment text NOT NULL,
    submit_date timestamp with time zone NOT NULL,
    ip_address inet,
    is_public boolean NOT NULL,
    is_removed boolean NOT NULL
);


ALTER TABLE public.django_comments OWNER TO gf_stage;

--
-- Name: django_comments_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE django_comments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_comments_id_seq OWNER TO gf_stage;

--
-- Name: django_comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE django_comments_id_seq OWNED BY django_comments.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO gf_stage;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO gf_stage;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO gf_stage;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO gf_stage;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_site_id_seq OWNER TO gf_stage;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE django_site_id_seq OWNED BY django_site.id;


--
-- Name: flexi_auth_param; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE flexi_auth_param (
    id integer NOT NULL,
    name character varying(20) NOT NULL,
    content_type_id integer NOT NULL,
    object_id integer NOT NULL,
    CONSTRAINT flexi_auth_param_object_id_check CHECK ((object_id >= 0))
);


ALTER TABLE public.flexi_auth_param OWNER TO gf_stage;

--
-- Name: flexi_auth_param_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE flexi_auth_param_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.flexi_auth_param_id_seq OWNER TO gf_stage;

--
-- Name: flexi_auth_param_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE flexi_auth_param_id_seq OWNED BY flexi_auth_param.id;


--
-- Name: flexi_auth_paramrole; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE flexi_auth_paramrole (
    id integer NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE public.flexi_auth_paramrole OWNER TO gf_stage;

--
-- Name: flexi_auth_paramrole_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE flexi_auth_paramrole_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.flexi_auth_paramrole_id_seq OWNER TO gf_stage;

--
-- Name: flexi_auth_paramrole_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE flexi_auth_paramrole_id_seq OWNED BY flexi_auth_paramrole.id;


--
-- Name: flexi_auth_paramrole_param_set; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE flexi_auth_paramrole_param_set (
    id integer NOT NULL,
    paramrole_id integer NOT NULL,
    param_id integer NOT NULL
);


ALTER TABLE public.flexi_auth_paramrole_param_set OWNER TO gf_stage;

--
-- Name: flexi_auth_paramrole_param_set_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE flexi_auth_paramrole_param_set_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.flexi_auth_paramrole_param_set_id_seq OWNER TO gf_stage;

--
-- Name: flexi_auth_paramrole_param_set_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE flexi_auth_paramrole_param_set_id_seq OWNED BY flexi_auth_paramrole_param_set.id;


--
-- Name: flexi_auth_principalparamrolerelation; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE flexi_auth_principalparamrolerelation (
    id integer NOT NULL,
    user_id integer,
    group_id integer,
    role_id integer NOT NULL
);


ALTER TABLE public.flexi_auth_principalparamrolerelation OWNER TO gf_stage;

--
-- Name: flexi_auth_principalparamrolerelation_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE flexi_auth_principalparamrolerelation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.flexi_auth_principalparamrolerelation_id_seq OWNER TO gf_stage;

--
-- Name: flexi_auth_principalparamrolerelation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE flexi_auth_principalparamrolerelation_id_seq OWNED BY flexi_auth_principalparamrolerelation.id;


--
-- Name: gas_delivery; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_delivery (
    id integer NOT NULL,
    place_id integer NOT NULL,
    date timestamp with time zone NOT NULL
);


ALTER TABLE public.gas_delivery OWNER TO gf_stage;

--
-- Name: gas_delivery_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_delivery_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_delivery_id_seq OWNER TO gf_stage;

--
-- Name: gas_delivery_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_delivery_id_seq OWNED BY gas_delivery.id;


--
-- Name: gas_gas; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_gas (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    id_in_des character varying(8) NOT NULL,
    logo character varying(100),
    headquarter_id integer NOT NULL,
    description text NOT NULL,
    membership_fee numeric(10,4) NOT NULL,
    birthday date,
    vat character varying(11) NOT NULL,
    fcc character varying(16) NOT NULL,
    orders_email_contact_id integer,
    website character varying(200),
    association_act character varying(100),
    intent_act character varying(100),
    note text NOT NULL,
    des_id integer NOT NULL
);


ALTER TABLE public.gas_gas OWNER TO gf_stage;

--
-- Name: gas_gas_contact_set; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_gas_contact_set (
    id integer NOT NULL,
    gas_id integer NOT NULL,
    contact_id integer NOT NULL
);


ALTER TABLE public.gas_gas_contact_set OWNER TO gf_stage;

--
-- Name: gas_gas_contact_set_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_gas_contact_set_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_gas_contact_set_id_seq OWNER TO gf_stage;

--
-- Name: gas_gas_contact_set_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_gas_contact_set_id_seq OWNED BY gas_gas_contact_set.id;


--
-- Name: gas_gas_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_gas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_gas_id_seq OWNER TO gf_stage;

--
-- Name: gas_gas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_gas_id_seq OWNED BY gas_gas.id;


--
-- Name: gas_gasactivist; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_gasactivist (
    id integer NOT NULL,
    gas_id integer NOT NULL,
    person_id integer NOT NULL,
    info_title character varying(256) NOT NULL,
    info_description text NOT NULL
);


ALTER TABLE public.gas_gasactivist OWNER TO gf_stage;

--
-- Name: gas_gasactivist_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_gasactivist_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_gasactivist_id_seq OWNER TO gf_stage;

--
-- Name: gas_gasactivist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_gasactivist_id_seq OWNED BY gas_gasactivist.id;


--
-- Name: gas_gasconfig; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_gasconfig (
    id integer NOT NULL,
    gas_id integer NOT NULL,
    default_workflow_gasmember_order_id integer NOT NULL,
    default_workflow_gassupplier_order_id integer NOT NULL,
    can_change_price boolean NOT NULL,
    order_show_only_next_delivery boolean NOT NULL,
    order_show_only_one_at_a_time boolean NOT NULL,
    default_close_day character varying(16) NOT NULL,
    default_delivery_day character varying(16) NOT NULL,
    default_close_time time without time zone,
    default_delivery_time time without time zone,
    use_withdrawal_place boolean NOT NULL,
    can_change_withdrawal_place_on_each_order boolean NOT NULL,
    can_change_delivery_place_on_each_order boolean NOT NULL,
    default_withdrawal_place_id integer,
    default_delivery_place_id integer,
    auto_populate_products boolean NOT NULL,
    use_scheduler boolean NOT NULL,
    gasmember_auto_confirm_order boolean NOT NULL,
    is_suspended boolean NOT NULL,
    suspend_datetime timestamp with time zone,
    suspend_reason text NOT NULL,
    suspend_auto_resume timestamp with time zone,
    notice_days_before_order_close integer,
    use_order_planning boolean NOT NULL,
    send_email_on_order_close boolean NOT NULL,
    registration_token character varying(32) NOT NULL,
    privacy_phone character varying(24) NOT NULL,
    privacy_email character varying(24) NOT NULL,
    privacy_cash character varying(24) NOT NULL,
    CONSTRAINT gas_gasconfig_notice_days_before_order_close_check CHECK ((notice_days_before_order_close >= 0))
);


ALTER TABLE public.gas_gasconfig OWNER TO gf_stage;

--
-- Name: gas_gasconfig_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_gasconfig_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_gasconfig_id_seq OWNER TO gf_stage;

--
-- Name: gas_gasconfig_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_gasconfig_id_seq OWNED BY gas_gasconfig.id;


--
-- Name: gas_gasconfig_intergas_connection_set; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_gasconfig_intergas_connection_set (
    id integer NOT NULL,
    gasconfig_id integer NOT NULL,
    gas_id integer NOT NULL
);


ALTER TABLE public.gas_gasconfig_intergas_connection_set OWNER TO gf_stage;

--
-- Name: gas_gasconfig_intergas_connection_set_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_gasconfig_intergas_connection_set_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_gasconfig_intergas_connection_set_id_seq OWNER TO gf_stage;

--
-- Name: gas_gasconfig_intergas_connection_set_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_gasconfig_intergas_connection_set_id_seq OWNED BY gas_gasconfig_intergas_connection_set.id;


--
-- Name: gas_gasmember; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_gasmember (
    id integer NOT NULL,
    person_id integer NOT NULL,
    gas_id integer NOT NULL,
    id_in_gas character varying(10),
    membership_fee_payed date,
    use_planned_list boolean NOT NULL,
    is_suspended boolean NOT NULL,
    suspend_datetime timestamp with time zone,
    suspend_reason text NOT NULL,
    suspend_auto_resume timestamp with time zone
);


ALTER TABLE public.gas_gasmember OWNER TO gf_stage;

--
-- Name: gas_gasmember_available_for_roles; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_gasmember_available_for_roles (
    id integer NOT NULL,
    gasmember_id integer NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE public.gas_gasmember_available_for_roles OWNER TO gf_stage;

--
-- Name: gas_gasmember_available_for_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_gasmember_available_for_roles_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_gasmember_available_for_roles_id_seq OWNER TO gf_stage;

--
-- Name: gas_gasmember_available_for_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_gasmember_available_for_roles_id_seq OWNED BY gas_gasmember_available_for_roles.id;


--
-- Name: gas_gasmember_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_gasmember_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_gasmember_id_seq OWNER TO gf_stage;

--
-- Name: gas_gasmember_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_gasmember_id_seq OWNED BY gas_gasmember.id;


--
-- Name: gas_gasmemberorder; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_gasmemberorder (
    id integer NOT NULL,
    purchaser_id integer NOT NULL,
    ordered_product_id integer NOT NULL,
    ordered_price numeric(10,4) NOT NULL,
    ordered_amount numeric(6,2) NOT NULL,
    withdrawn_amount numeric(6,2),
    is_confirmed boolean NOT NULL,
    note character varying(64)
);


ALTER TABLE public.gas_gasmemberorder OWNER TO gf_stage;

--
-- Name: gas_gasmemberorder_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_gasmemberorder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_gasmemberorder_id_seq OWNER TO gf_stage;

--
-- Name: gas_gasmemberorder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_gasmemberorder_id_seq OWNED BY gas_gasmemberorder.id;


--
-- Name: gas_gassupplierorder; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_gassupplierorder (
    id integer NOT NULL,
    pact_id integer NOT NULL,
    datetime_start timestamp with time zone NOT NULL,
    datetime_end timestamp with time zone,
    order_minimum_amount numeric(10,4),
    delivery_id integer,
    withdrawal_id integer,
    delivery_cost numeric(10,4),
    referrer_person_id integer,
    delivery_referrer_person_id integer,
    withdrawal_referrer_person_id integer,
    group_id integer,
    invoice_amount numeric(10,4),
    invoice_note text NOT NULL,
    root_plan_id integer,
    CONSTRAINT gas_gassupplierorder_group_id_check CHECK ((group_id >= 0))
);


ALTER TABLE public.gas_gassupplierorder OWNER TO gf_stage;

--
-- Name: gas_gassupplierorder_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_gassupplierorder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_gassupplierorder_id_seq OWNER TO gf_stage;

--
-- Name: gas_gassupplierorder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_gassupplierorder_id_seq OWNED BY gas_gassupplierorder.id;


--
-- Name: gas_gassupplierorderproduct; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_gassupplierorderproduct (
    id integer NOT NULL,
    order_id integer NOT NULL,
    gasstock_id integer NOT NULL,
    maximum_amount numeric(8,2),
    initial_price numeric(10,4) NOT NULL,
    order_price numeric(10,4) NOT NULL,
    delivered_price numeric(10,4),
    delivered_amount numeric(8,2)
);


ALTER TABLE public.gas_gassupplierorderproduct OWNER TO gf_stage;

--
-- Name: gas_gassupplierorderproduct_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_gassupplierorderproduct_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_gassupplierorderproduct_id_seq OWNER TO gf_stage;

--
-- Name: gas_gassupplierorderproduct_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_gassupplierorderproduct_id_seq OWNED BY gas_gassupplierorderproduct.id;


--
-- Name: gas_gassuppliersolidalpact; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_gassuppliersolidalpact (
    id integer NOT NULL,
    gas_id integer NOT NULL,
    supplier_id integer NOT NULL,
    date_signed date,
    order_minimum_amount numeric(10,4),
    order_delivery_cost numeric(10,4),
    order_deliver_interval time without time zone,
    order_price_percent_update numeric(3,2),
    default_delivery_day character varying(16) NOT NULL,
    default_delivery_time time without time zone,
    default_delivery_place_id integer,
    auto_populate_products boolean NOT NULL,
    orders_can_be_grouped boolean NOT NULL,
    document character varying(100),
    is_suspended boolean NOT NULL,
    suspend_datetime timestamp with time zone,
    suspend_reason text NOT NULL,
    suspend_auto_resume timestamp with time zone,
    send_email_on_order_close boolean NOT NULL
);


ALTER TABLE public.gas_gassuppliersolidalpact OWNER TO gf_stage;

--
-- Name: gas_gassuppliersolidalpact_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_gassuppliersolidalpact_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_gassuppliersolidalpact_id_seq OWNER TO gf_stage;

--
-- Name: gas_gassuppliersolidalpact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_gassuppliersolidalpact_id_seq OWNED BY gas_gassuppliersolidalpact.id;


--
-- Name: gas_gassupplierstock; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_gassupplierstock (
    id integer NOT NULL,
    pact_id integer NOT NULL,
    stock_id integer NOT NULL,
    enabled boolean NOT NULL,
    minimum_amount numeric(5,2) NOT NULL,
    step numeric(5,2) NOT NULL
);


ALTER TABLE public.gas_gassupplierstock OWNER TO gf_stage;

--
-- Name: gas_gassupplierstock_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_gassupplierstock_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_gassupplierstock_id_seq OWNER TO gf_stage;

--
-- Name: gas_gassupplierstock_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_gassupplierstock_id_seq OWNED BY gas_gassupplierstock.id;


--
-- Name: gas_historicaldelivery; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_historicaldelivery (
    id integer NOT NULL,
    place_id integer,
    date timestamp with time zone NOT NULL,
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL
);


ALTER TABLE public.gas_historicaldelivery OWNER TO gf_stage;

--
-- Name: gas_historicaldelivery_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_historicaldelivery_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_historicaldelivery_history_id_seq OWNER TO gf_stage;

--
-- Name: gas_historicaldelivery_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_historicaldelivery_history_id_seq OWNED BY gas_historicaldelivery.history_id;


--
-- Name: gas_historicalgas; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_historicalgas (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    id_in_des character varying(8) NOT NULL,
    logo character varying(100),
    headquarter_id integer,
    description text NOT NULL,
    membership_fee numeric(10,4) NOT NULL,
    birthday date,
    vat character varying(11) NOT NULL,
    fcc character varying(16) NOT NULL,
    orders_email_contact_id integer,
    website character varying(200),
    association_act character varying(100),
    intent_act character varying(100),
    note text NOT NULL,
    des_id integer,
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL
);


ALTER TABLE public.gas_historicalgas OWNER TO gf_stage;

--
-- Name: gas_historicalgas_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_historicalgas_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_historicalgas_history_id_seq OWNER TO gf_stage;

--
-- Name: gas_historicalgas_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_historicalgas_history_id_seq OWNED BY gas_historicalgas.history_id;


--
-- Name: gas_historicalgasactivist; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_historicalgasactivist (
    id integer NOT NULL,
    gas_id integer,
    person_id integer,
    info_title character varying(256) NOT NULL,
    info_description text NOT NULL,
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL
);


ALTER TABLE public.gas_historicalgasactivist OWNER TO gf_stage;

--
-- Name: gas_historicalgasactivist_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_historicalgasactivist_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_historicalgasactivist_history_id_seq OWNER TO gf_stage;

--
-- Name: gas_historicalgasactivist_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_historicalgasactivist_history_id_seq OWNED BY gas_historicalgasactivist.history_id;


--
-- Name: gas_historicalgasconfig; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_historicalgasconfig (
    id integer NOT NULL,
    gas_id integer,
    default_workflow_gasmember_order_id integer,
    default_workflow_gassupplier_order_id integer,
    can_change_price boolean NOT NULL,
    order_show_only_next_delivery boolean NOT NULL,
    order_show_only_one_at_a_time boolean NOT NULL,
    default_close_day character varying(16) NOT NULL,
    default_delivery_day character varying(16) NOT NULL,
    default_close_time time without time zone,
    default_delivery_time time without time zone,
    use_withdrawal_place boolean NOT NULL,
    can_change_withdrawal_place_on_each_order boolean NOT NULL,
    can_change_delivery_place_on_each_order boolean NOT NULL,
    default_withdrawal_place_id integer,
    default_delivery_place_id integer,
    auto_populate_products boolean NOT NULL,
    use_scheduler boolean NOT NULL,
    gasmember_auto_confirm_order boolean NOT NULL,
    is_suspended boolean NOT NULL,
    suspend_datetime timestamp with time zone,
    suspend_reason text NOT NULL,
    suspend_auto_resume timestamp with time zone,
    notice_days_before_order_close integer,
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL,
    use_order_planning boolean NOT NULL,
    send_email_on_order_close boolean NOT NULL,
    registration_token character varying(32) NOT NULL,
    privacy_phone character varying(24) NOT NULL,
    privacy_email character varying(24) NOT NULL,
    privacy_cash character varying(24) NOT NULL,
    CONSTRAINT gas_historicalgasconfig_notice_days_before_order_close_check CHECK ((notice_days_before_order_close >= 0))
);


ALTER TABLE public.gas_historicalgasconfig OWNER TO gf_stage;

--
-- Name: gas_historicalgasconfig_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_historicalgasconfig_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_historicalgasconfig_history_id_seq OWNER TO gf_stage;

--
-- Name: gas_historicalgasconfig_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_historicalgasconfig_history_id_seq OWNED BY gas_historicalgasconfig.history_id;


--
-- Name: gas_historicalgasmember; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_historicalgasmember (
    id integer NOT NULL,
    person_id integer,
    gas_id integer,
    id_in_gas character varying(10),
    membership_fee_payed date,
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL,
    use_planned_list boolean NOT NULL,
    is_suspended boolean NOT NULL,
    suspend_datetime timestamp with time zone,
    suspend_reason text NOT NULL,
    suspend_auto_resume timestamp with time zone
);


ALTER TABLE public.gas_historicalgasmember OWNER TO gf_stage;

--
-- Name: gas_historicalgasmember_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_historicalgasmember_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_historicalgasmember_history_id_seq OWNER TO gf_stage;

--
-- Name: gas_historicalgasmember_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_historicalgasmember_history_id_seq OWNED BY gas_historicalgasmember.history_id;


--
-- Name: gas_historicalgasmemberorder; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_historicalgasmemberorder (
    id integer NOT NULL,
    purchaser_id integer,
    ordered_product_id integer,
    ordered_price numeric(10,4) NOT NULL,
    ordered_amount numeric(6,2) NOT NULL,
    withdrawn_amount numeric(6,2),
    is_confirmed boolean NOT NULL,
    note character varying(64),
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL
);


ALTER TABLE public.gas_historicalgasmemberorder OWNER TO gf_stage;

--
-- Name: gas_historicalgasmemberorder_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_historicalgasmemberorder_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_historicalgasmemberorder_history_id_seq OWNER TO gf_stage;

--
-- Name: gas_historicalgasmemberorder_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_historicalgasmemberorder_history_id_seq OWNED BY gas_historicalgasmemberorder.history_id;


--
-- Name: gas_historicalgassupplierorder; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_historicalgassupplierorder (
    id integer NOT NULL,
    pact_id integer,
    datetime_start timestamp with time zone NOT NULL,
    datetime_end timestamp with time zone,
    order_minimum_amount numeric(10,4),
    delivery_id integer,
    withdrawal_id integer,
    delivery_cost numeric(10,4),
    referrer_person_id integer,
    delivery_referrer_person_id integer,
    withdrawal_referrer_person_id integer,
    group_id integer,
    invoice_amount numeric(10,4),
    invoice_note text NOT NULL,
    root_plan_id integer,
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL,
    CONSTRAINT gas_historicalgassupplierorder_group_id_check CHECK ((group_id >= 0))
);


ALTER TABLE public.gas_historicalgassupplierorder OWNER TO gf_stage;

--
-- Name: gas_historicalgassupplierorder_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_historicalgassupplierorder_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_historicalgassupplierorder_history_id_seq OWNER TO gf_stage;

--
-- Name: gas_historicalgassupplierorder_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_historicalgassupplierorder_history_id_seq OWNED BY gas_historicalgassupplierorder.history_id;


--
-- Name: gas_historicalgassupplierorderproduct; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_historicalgassupplierorderproduct (
    id integer NOT NULL,
    order_id integer,
    gasstock_id integer,
    maximum_amount numeric(8,2),
    initial_price numeric(10,4) NOT NULL,
    order_price numeric(10,4) NOT NULL,
    delivered_price numeric(10,4),
    delivered_amount numeric(8,2),
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL
);


ALTER TABLE public.gas_historicalgassupplierorderproduct OWNER TO gf_stage;

--
-- Name: gas_historicalgassupplierorderproduct_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_historicalgassupplierorderproduct_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_historicalgassupplierorderproduct_history_id_seq OWNER TO gf_stage;

--
-- Name: gas_historicalgassupplierorderproduct_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_historicalgassupplierorderproduct_history_id_seq OWNED BY gas_historicalgassupplierorderproduct.history_id;


--
-- Name: gas_historicalgassuppliersolidalpact; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_historicalgassuppliersolidalpact (
    id integer NOT NULL,
    gas_id integer,
    supplier_id integer,
    date_signed date,
    order_minimum_amount numeric(10,4),
    order_delivery_cost numeric(10,4),
    order_deliver_interval time without time zone,
    order_price_percent_update numeric(3,2),
    default_delivery_day character varying(16) NOT NULL,
    default_delivery_time time without time zone,
    default_delivery_place_id integer,
    auto_populate_products boolean NOT NULL,
    orders_can_be_grouped boolean NOT NULL,
    document character varying(100),
    is_suspended boolean NOT NULL,
    suspend_datetime timestamp with time zone,
    suspend_reason text NOT NULL,
    suspend_auto_resume timestamp with time zone,
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL,
    send_email_on_order_close boolean NOT NULL
);


ALTER TABLE public.gas_historicalgassuppliersolidalpact OWNER TO gf_stage;

--
-- Name: gas_historicalgassuppliersolidalpact_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_historicalgassuppliersolidalpact_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_historicalgassuppliersolidalpact_history_id_seq OWNER TO gf_stage;

--
-- Name: gas_historicalgassuppliersolidalpact_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_historicalgassuppliersolidalpact_history_id_seq OWNED BY gas_historicalgassuppliersolidalpact.history_id;


--
-- Name: gas_historicalgassupplierstock; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_historicalgassupplierstock (
    id integer NOT NULL,
    pact_id integer,
    stock_id integer,
    enabled boolean NOT NULL,
    minimum_amount numeric(5,2) NOT NULL,
    step numeric(5,2) NOT NULL,
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL
);


ALTER TABLE public.gas_historicalgassupplierstock OWNER TO gf_stage;

--
-- Name: gas_historicalgassupplierstock_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_historicalgassupplierstock_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_historicalgassupplierstock_history_id_seq OWNER TO gf_stage;

--
-- Name: gas_historicalgassupplierstock_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_historicalgassupplierstock_history_id_seq OWNED BY gas_historicalgassupplierstock.history_id;


--
-- Name: gas_historicalwithdrawal; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_historicalwithdrawal (
    id integer NOT NULL,
    place_id integer,
    date timestamp with time zone NOT NULL,
    start_time time without time zone NOT NULL,
    end_time time without time zone NOT NULL,
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL
);


ALTER TABLE public.gas_historicalwithdrawal OWNER TO gf_stage;

--
-- Name: gas_historicalwithdrawal_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_historicalwithdrawal_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_historicalwithdrawal_history_id_seq OWNER TO gf_stage;

--
-- Name: gas_historicalwithdrawal_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_historicalwithdrawal_history_id_seq OWNED BY gas_historicalwithdrawal.history_id;


--
-- Name: gas_withdrawal; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE gas_withdrawal (
    id integer NOT NULL,
    place_id integer NOT NULL,
    date timestamp with time zone NOT NULL,
    start_time time without time zone NOT NULL,
    end_time time without time zone NOT NULL
);


ALTER TABLE public.gas_withdrawal OWNER TO gf_stage;

--
-- Name: gas_withdrawal_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE gas_withdrawal_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.gas_withdrawal_id_seq OWNER TO gf_stage;

--
-- Name: gas_withdrawal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE gas_withdrawal_id_seq OWNED BY gas_withdrawal.id;


--
-- Name: notification_notice; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE notification_notice (
    id integer NOT NULL,
    recipient_id integer NOT NULL,
    sender_id integer,
    message text NOT NULL,
    notice_type_id integer NOT NULL,
    added timestamp with time zone NOT NULL,
    unseen boolean NOT NULL,
    archived boolean NOT NULL,
    on_site boolean NOT NULL
);


ALTER TABLE public.notification_notice OWNER TO gf_stage;

--
-- Name: notification_notice_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE notification_notice_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notification_notice_id_seq OWNER TO gf_stage;

--
-- Name: notification_notice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE notification_notice_id_seq OWNED BY notification_notice.id;


--
-- Name: notification_noticequeuebatch; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE notification_noticequeuebatch (
    id integer NOT NULL,
    pickled_data text NOT NULL
);


ALTER TABLE public.notification_noticequeuebatch OWNER TO gf_stage;

--
-- Name: notification_noticequeuebatch_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE notification_noticequeuebatch_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notification_noticequeuebatch_id_seq OWNER TO gf_stage;

--
-- Name: notification_noticequeuebatch_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE notification_noticequeuebatch_id_seq OWNED BY notification_noticequeuebatch.id;


--
-- Name: notification_noticesetting; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE notification_noticesetting (
    id integer NOT NULL,
    user_id integer NOT NULL,
    notice_type_id integer NOT NULL,
    medium character varying(1) NOT NULL,
    send boolean NOT NULL
);


ALTER TABLE public.notification_noticesetting OWNER TO gf_stage;

--
-- Name: notification_noticesetting_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE notification_noticesetting_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notification_noticesetting_id_seq OWNER TO gf_stage;

--
-- Name: notification_noticesetting_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE notification_noticesetting_id_seq OWNED BY notification_noticesetting.id;


--
-- Name: notification_noticetype; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE notification_noticetype (
    id integer NOT NULL,
    label character varying(40) NOT NULL,
    display character varying(50) NOT NULL,
    description character varying(100) NOT NULL,
    "default" integer NOT NULL
);


ALTER TABLE public.notification_noticetype OWNER TO gf_stage;

--
-- Name: notification_noticetype_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE notification_noticetype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notification_noticetype_id_seq OWNER TO gf_stage;

--
-- Name: notification_noticetype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE notification_noticetype_id_seq OWNED BY notification_noticetype.id;


--
-- Name: notification_observeditem; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE notification_observeditem (
    id integer NOT NULL,
    user_id integer NOT NULL,
    content_type_id integer NOT NULL,
    object_id integer NOT NULL,
    notice_type_id integer NOT NULL,
    added timestamp with time zone NOT NULL,
    signal text NOT NULL,
    CONSTRAINT notification_observeditem_object_id_check CHECK ((object_id >= 0))
);


ALTER TABLE public.notification_observeditem OWNER TO gf_stage;

--
-- Name: notification_observeditem_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE notification_observeditem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notification_observeditem_id_seq OWNER TO gf_stage;

--
-- Name: notification_observeditem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE notification_observeditem_id_seq OWNED BY notification_observeditem.id;


--
-- Name: permissions_objectpermission; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE permissions_objectpermission (
    id integer NOT NULL,
    role_id integer,
    permission_id integer NOT NULL,
    content_type_id integer NOT NULL,
    content_id integer NOT NULL,
    CONSTRAINT permissions_objectpermission_content_id_check CHECK ((content_id >= 0))
);


ALTER TABLE public.permissions_objectpermission OWNER TO gf_stage;

--
-- Name: permissions_objectpermission_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE permissions_objectpermission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.permissions_objectpermission_id_seq OWNER TO gf_stage;

--
-- Name: permissions_objectpermission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE permissions_objectpermission_id_seq OWNED BY permissions_objectpermission.id;


--
-- Name: permissions_objectpermissioninheritanceblock; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE permissions_objectpermissioninheritanceblock (
    id integer NOT NULL,
    permission_id integer NOT NULL,
    content_type_id integer NOT NULL,
    content_id integer NOT NULL,
    CONSTRAINT permissions_objectpermissioninheritanceblock_content_id_check CHECK ((content_id >= 0))
);


ALTER TABLE public.permissions_objectpermissioninheritanceblock OWNER TO gf_stage;

--
-- Name: permissions_objectpermissioninheritanceblock_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE permissions_objectpermissioninheritanceblock_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.permissions_objectpermissioninheritanceblock_id_seq OWNER TO gf_stage;

--
-- Name: permissions_objectpermissioninheritanceblock_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE permissions_objectpermissioninheritanceblock_id_seq OWNED BY permissions_objectpermissioninheritanceblock.id;


--
-- Name: permissions_permission; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE permissions_permission (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.permissions_permission OWNER TO gf_stage;

--
-- Name: permissions_permission_content_types; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE permissions_permission_content_types (
    id integer NOT NULL,
    permission_id integer NOT NULL,
    contenttype_id integer NOT NULL
);


ALTER TABLE public.permissions_permission_content_types OWNER TO gf_stage;

--
-- Name: permissions_permission_content_types_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE permissions_permission_content_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.permissions_permission_content_types_id_seq OWNER TO gf_stage;

--
-- Name: permissions_permission_content_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE permissions_permission_content_types_id_seq OWNED BY permissions_permission_content_types.id;


--
-- Name: permissions_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE permissions_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.permissions_permission_id_seq OWNER TO gf_stage;

--
-- Name: permissions_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE permissions_permission_id_seq OWNED BY permissions_permission.id;


--
-- Name: permissions_principalrolerelation; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE permissions_principalrolerelation (
    id integer NOT NULL,
    user_id integer,
    group_id integer,
    role_id integer NOT NULL,
    content_type_id integer,
    content_id integer,
    CONSTRAINT permissions_principalrolerelation_content_id_check CHECK ((content_id >= 0))
);


ALTER TABLE public.permissions_principalrolerelation OWNER TO gf_stage;

--
-- Name: permissions_principalrolerelation_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE permissions_principalrolerelation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.permissions_principalrolerelation_id_seq OWNER TO gf_stage;

--
-- Name: permissions_principalrolerelation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE permissions_principalrolerelation_id_seq OWNED BY permissions_principalrolerelation.id;


--
-- Name: permissions_role; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE permissions_role (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.permissions_role OWNER TO gf_stage;

--
-- Name: permissions_role_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE permissions_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.permissions_role_id_seq OWNER TO gf_stage;

--
-- Name: permissions_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE permissions_role_id_seq OWNED BY permissions_role.id;


--
-- Name: registration_registrationprofile; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE registration_registrationprofile (
    id integer NOT NULL,
    user_id integer NOT NULL,
    activation_key character varying(40) NOT NULL
);


ALTER TABLE public.registration_registrationprofile OWNER TO gf_stage;

--
-- Name: registration_registrationprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE registration_registrationprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.registration_registrationprofile_id_seq OWNER TO gf_stage;

--
-- Name: registration_registrationprofile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE registration_registrationprofile_id_seq OWNED BY registration_registrationprofile.id;


--
-- Name: rest_homepage; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE rest_homepage (
    id integer NOT NULL,
    role_id integer NOT NULL,
    user_id integer NOT NULL,
    resource_ctype_id integer NOT NULL,
    resource_id integer NOT NULL,
    CONSTRAINT rest_homepage_resource_id_check CHECK ((resource_id >= 0))
);


ALTER TABLE public.rest_homepage OWNER TO gf_stage;

--
-- Name: rest_homepage_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE rest_homepage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rest_homepage_id_seq OWNER TO gf_stage;

--
-- Name: rest_homepage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE rest_homepage_id_seq OWNED BY rest_homepage.id;


--
-- Name: rest_page; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE rest_page (
    id integer NOT NULL,
    role_id integer NOT NULL,
    user_id integer,
    resource_ctype_id integer NOT NULL,
    resource_id integer,
    confdata text,
    CONSTRAINT rest_page_resource_id_check CHECK ((resource_id >= 0))
);


ALTER TABLE public.rest_page OWNER TO gf_stage;

--
-- Name: rest_page_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE rest_page_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rest_page_id_seq OWNER TO gf_stage;

--
-- Name: rest_page_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE rest_page_id_seq OWNED BY rest_page.id;


--
-- Name: simple_accounting_account; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE simple_accounting_account (
    id integer NOT NULL,
    system_id integer NOT NULL,
    parent_id integer,
    name character varying(128) NOT NULL,
    kind_id integer NOT NULL,
    is_placeholder boolean NOT NULL
);


ALTER TABLE public.simple_accounting_account OWNER TO gf_stage;

--
-- Name: simple_accounting_account_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE simple_accounting_account_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.simple_accounting_account_id_seq OWNER TO gf_stage;

--
-- Name: simple_accounting_account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE simple_accounting_account_id_seq OWNED BY simple_accounting_account.id;


--
-- Name: simple_accounting_accountsystem; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE simple_accounting_accountsystem (
    id integer NOT NULL,
    owner_id integer NOT NULL
);


ALTER TABLE public.simple_accounting_accountsystem OWNER TO gf_stage;

--
-- Name: simple_accounting_accountsystem_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE simple_accounting_accountsystem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.simple_accounting_accountsystem_id_seq OWNER TO gf_stage;

--
-- Name: simple_accounting_accountsystem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE simple_accounting_accountsystem_id_seq OWNED BY simple_accounting_accountsystem.id;


--
-- Name: simple_accounting_accounttype; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE simple_accounting_accounttype (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    base_type integer NOT NULL
);


ALTER TABLE public.simple_accounting_accounttype OWNER TO gf_stage;

--
-- Name: simple_accounting_accounttype_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE simple_accounting_accounttype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.simple_accounting_accounttype_id_seq OWNER TO gf_stage;

--
-- Name: simple_accounting_accounttype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE simple_accounting_accounttype_id_seq OWNED BY simple_accounting_accounttype.id;


--
-- Name: simple_accounting_cashflow; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE simple_accounting_cashflow (
    id integer NOT NULL,
    account_id integer NOT NULL,
    amount numeric(10,4) NOT NULL
);


ALTER TABLE public.simple_accounting_cashflow OWNER TO gf_stage;

--
-- Name: simple_accounting_cashflow_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE simple_accounting_cashflow_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.simple_accounting_cashflow_id_seq OWNER TO gf_stage;

--
-- Name: simple_accounting_cashflow_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE simple_accounting_cashflow_id_seq OWNED BY simple_accounting_cashflow.id;


--
-- Name: simple_accounting_invoice; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE simple_accounting_invoice (
    id integer NOT NULL,
    issuer_id integer NOT NULL,
    recipient_id integer NOT NULL,
    net_amount numeric(10,4) NOT NULL,
    taxes numeric(10,4),
    issue_date timestamp with time zone NOT NULL,
    due_date timestamp with time zone NOT NULL,
    status integer NOT NULL,
    document character varying(100) NOT NULL
);


ALTER TABLE public.simple_accounting_invoice OWNER TO gf_stage;

--
-- Name: simple_accounting_invoice_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE simple_accounting_invoice_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.simple_accounting_invoice_id_seq OWNER TO gf_stage;

--
-- Name: simple_accounting_invoice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE simple_accounting_invoice_id_seq OWNED BY simple_accounting_invoice.id;


--
-- Name: simple_accounting_ledgerentry; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE simple_accounting_ledgerentry (
    id integer NOT NULL,
    account_id integer NOT NULL,
    transaction_id integer NOT NULL,
    entry_id integer,
    amount numeric(10,4) NOT NULL,
    balance_current numeric(10,4),
    CONSTRAINT simple_accounting_ledgerentry_entry_id_check CHECK ((entry_id >= 0))
);


ALTER TABLE public.simple_accounting_ledgerentry OWNER TO gf_stage;

--
-- Name: simple_accounting_ledgerentry_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE simple_accounting_ledgerentry_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.simple_accounting_ledgerentry_id_seq OWNER TO gf_stage;

--
-- Name: simple_accounting_ledgerentry_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE simple_accounting_ledgerentry_id_seq OWNED BY simple_accounting_ledgerentry.id;


--
-- Name: simple_accounting_split; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE simple_accounting_split (
    id integer NOT NULL,
    exit_point_id integer,
    entry_point_id integer,
    target_id integer NOT NULL,
    description character varying(512) NOT NULL
);


ALTER TABLE public.simple_accounting_split OWNER TO gf_stage;

--
-- Name: simple_accounting_split_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE simple_accounting_split_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.simple_accounting_split_id_seq OWNER TO gf_stage;

--
-- Name: simple_accounting_split_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE simple_accounting_split_id_seq OWNED BY simple_accounting_split.id;


--
-- Name: simple_accounting_subject; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE simple_accounting_subject (
    id integer NOT NULL,
    content_type_id integer NOT NULL,
    object_id integer NOT NULL,
    CONSTRAINT simple_accounting_subject_object_id_check CHECK ((object_id >= 0))
);


ALTER TABLE public.simple_accounting_subject OWNER TO gf_stage;

--
-- Name: simple_accounting_subject_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE simple_accounting_subject_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.simple_accounting_subject_id_seq OWNER TO gf_stage;

--
-- Name: simple_accounting_subject_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE simple_accounting_subject_id_seq OWNED BY simple_accounting_subject.id;


--
-- Name: simple_accounting_transaction; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE simple_accounting_transaction (
    id integer NOT NULL,
    date timestamp with time zone NOT NULL,
    description character varying(512) NOT NULL,
    issuer_id integer NOT NULL,
    source_id integer NOT NULL,
    kind character varying(128),
    is_confirmed boolean NOT NULL
);


ALTER TABLE public.simple_accounting_transaction OWNER TO gf_stage;

--
-- Name: simple_accounting_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE simple_accounting_transaction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.simple_accounting_transaction_id_seq OWNER TO gf_stage;

--
-- Name: simple_accounting_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE simple_accounting_transaction_id_seq OWNED BY simple_accounting_transaction.id;


--
-- Name: simple_accounting_transaction_split_set; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE simple_accounting_transaction_split_set (
    id integer NOT NULL,
    transaction_id integer NOT NULL,
    split_id integer NOT NULL
);


ALTER TABLE public.simple_accounting_transaction_split_set OWNER TO gf_stage;

--
-- Name: simple_accounting_transaction_split_set_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE simple_accounting_transaction_split_set_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.simple_accounting_transaction_split_set_id_seq OWNER TO gf_stage;

--
-- Name: simple_accounting_transaction_split_set_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE simple_accounting_transaction_split_set_id_seq OWNED BY simple_accounting_transaction_split_set.id;


--
-- Name: simple_accounting_transactionreference; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE simple_accounting_transactionreference (
    id integer NOT NULL,
    transaction_id integer NOT NULL,
    content_type_id integer NOT NULL,
    object_id integer NOT NULL,
    CONSTRAINT simple_accounting_transactionreference_object_id_check CHECK ((object_id >= 0))
);


ALTER TABLE public.simple_accounting_transactionreference OWNER TO gf_stage;

--
-- Name: simple_accounting_transactionreference_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE simple_accounting_transactionreference_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.simple_accounting_transactionreference_id_seq OWNER TO gf_stage;

--
-- Name: simple_accounting_transactionreference_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE simple_accounting_transactionreference_id_seq OWNED BY simple_accounting_transactionreference.id;


--
-- Name: south_migrationhistory; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE south_migrationhistory (
    id integer NOT NULL,
    app_name character varying(255) NOT NULL,
    migration character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.south_migrationhistory OWNER TO gf_stage;

--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE south_migrationhistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.south_migrationhistory_id_seq OWNER TO gf_stage;

--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE south_migrationhistory_id_seq OWNED BY south_migrationhistory.id;


--
-- Name: supplier_certification; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_certification (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    symbol character varying(5) NOT NULL,
    description text NOT NULL
);


ALTER TABLE public.supplier_certification OWNER TO gf_stage;

--
-- Name: supplier_certification_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_certification_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_certification_id_seq OWNER TO gf_stage;

--
-- Name: supplier_certification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_certification_id_seq OWNED BY supplier_certification.id;


--
-- Name: supplier_historicalcertification; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_historicalcertification (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    symbol character varying(5) NOT NULL,
    description text NOT NULL,
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL
);


ALTER TABLE public.supplier_historicalcertification OWNER TO gf_stage;

--
-- Name: supplier_historicalcertification_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_historicalcertification_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_historicalcertification_history_id_seq OWNER TO gf_stage;

--
-- Name: supplier_historicalcertification_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_historicalcertification_history_id_seq OWNED BY supplier_historicalcertification.history_id;


--
-- Name: supplier_historicalproduct; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_historicalproduct (
    id integer NOT NULL,
    code character varying(128),
    producer_id integer NOT NULL,
    category_id integer NOT NULL,
    mu_id integer,
    pu_id integer NOT NULL,
    muppu numeric(6,2),
    muppu_is_variable boolean NOT NULL,
    vat_percent numeric(3,2) NOT NULL,
    name character varying(128) NOT NULL,
    description text NOT NULL,
    deleted boolean NOT NULL,
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL
);


ALTER TABLE public.supplier_historicalproduct OWNER TO gf_stage;

--
-- Name: supplier_historicalproduct_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_historicalproduct_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_historicalproduct_history_id_seq OWNER TO gf_stage;

--
-- Name: supplier_historicalproduct_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_historicalproduct_history_id_seq OWNED BY supplier_historicalproduct.history_id;


--
-- Name: supplier_historicalproductcategory; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_historicalproductcategory (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    description text NOT NULL,
    image character varying(100),
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL
);


ALTER TABLE public.supplier_historicalproductcategory OWNER TO gf_stage;

--
-- Name: supplier_historicalproductcategory_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_historicalproductcategory_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_historicalproductcategory_history_id_seq OWNER TO gf_stage;

--
-- Name: supplier_historicalproductcategory_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_historicalproductcategory_history_id_seq OWNED BY supplier_historicalproductcategory.history_id;


--
-- Name: supplier_historicalproductmu; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_historicalproductmu (
    id integer NOT NULL,
    name character varying(32) NOT NULL,
    symbol character varying(5) NOT NULL,
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL
);


ALTER TABLE public.supplier_historicalproductmu OWNER TO gf_stage;

--
-- Name: supplier_historicalproductmu_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_historicalproductmu_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_historicalproductmu_history_id_seq OWNER TO gf_stage;

--
-- Name: supplier_historicalproductmu_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_historicalproductmu_history_id_seq OWNED BY supplier_historicalproductmu.history_id;


--
-- Name: supplier_historicalproductpu; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_historicalproductpu (
    id integer NOT NULL,
    name character varying(32) NOT NULL,
    symbol character varying(5) NOT NULL,
    description text NOT NULL,
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL
);


ALTER TABLE public.supplier_historicalproductpu OWNER TO gf_stage;

--
-- Name: supplier_historicalproductpu_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_historicalproductpu_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_historicalproductpu_history_id_seq OWNER TO gf_stage;

--
-- Name: supplier_historicalproductpu_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_historicalproductpu_history_id_seq OWNED BY supplier_historicalproductpu.history_id;


--
-- Name: supplier_historicalsupplier; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_historicalsupplier (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    seat_id integer,
    vat_number character varying(128),
    ssn character varying(128),
    website character varying(200) NOT NULL,
    frontman_id integer,
    flavour character varying(128) NOT NULL,
    n_employers integer,
    logo character varying(100),
    iban character varying(64) NOT NULL,
    description text NOT NULL,
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL,
    CONSTRAINT supplier_historicalsupplier_n_employers_check CHECK ((n_employers >= 0))
);


ALTER TABLE public.supplier_historicalsupplier OWNER TO gf_stage;

--
-- Name: supplier_historicalsupplier_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_historicalsupplier_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_historicalsupplier_history_id_seq OWNER TO gf_stage;

--
-- Name: supplier_historicalsupplier_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_historicalsupplier_history_id_seq OWNED BY supplier_historicalsupplier.history_id;


--
-- Name: supplier_historicalsupplieragent; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_historicalsupplieragent (
    id integer NOT NULL,
    supplier_id integer NOT NULL,
    person_id integer NOT NULL,
    job_title character varying(256) NOT NULL,
    job_description text NOT NULL,
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL
);


ALTER TABLE public.supplier_historicalsupplieragent OWNER TO gf_stage;

--
-- Name: supplier_historicalsupplieragent_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_historicalsupplieragent_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_historicalsupplieragent_history_id_seq OWNER TO gf_stage;

--
-- Name: supplier_historicalsupplieragent_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_historicalsupplieragent_history_id_seq OWNED BY supplier_historicalsupplieragent.history_id;


--
-- Name: supplier_historicalsupplierstock; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_historicalsupplierstock (
    id integer NOT NULL,
    supplier_id integer NOT NULL,
    product_id integer NOT NULL,
    supplier_category_id integer,
    image character varying(100),
    price numeric(10,4) NOT NULL,
    code character varying(128),
    amount_available integer NOT NULL,
    units_minimum_amount integer NOT NULL,
    units_per_box numeric(5,2) NOT NULL,
    detail_minimum_amount numeric(5,2),
    detail_step numeric(5,2),
    delivery_notes text NOT NULL,
    deleted boolean NOT NULL,
    history_id integer NOT NULL,
    history_date timestamp with time zone NOT NULL,
    history_user_id integer,
    history_type character varying(1) NOT NULL,
    CONSTRAINT supplier_historicalsupplierstock_amount_available_check CHECK ((amount_available >= 0)),
    CONSTRAINT supplier_historicalsupplierstock_units_minimum_amount_check CHECK ((units_minimum_amount >= 0))
);


ALTER TABLE public.supplier_historicalsupplierstock OWNER TO gf_stage;

--
-- Name: supplier_historicalsupplierstock_history_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_historicalsupplierstock_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_historicalsupplierstock_history_id_seq OWNER TO gf_stage;

--
-- Name: supplier_historicalsupplierstock_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_historicalsupplierstock_history_id_seq OWNED BY supplier_historicalsupplierstock.history_id;


--
-- Name: supplier_product; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_product (
    id integer NOT NULL,
    code character varying(128),
    producer_id integer NOT NULL,
    category_id integer NOT NULL,
    mu_id integer,
    pu_id integer NOT NULL,
    muppu numeric(6,2),
    muppu_is_variable boolean NOT NULL,
    vat_percent numeric(3,2) NOT NULL,
    name character varying(128) NOT NULL,
    description text NOT NULL,
    deleted boolean NOT NULL
);


ALTER TABLE public.supplier_product OWNER TO gf_stage;

--
-- Name: supplier_product_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_product_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_product_id_seq OWNER TO gf_stage;

--
-- Name: supplier_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_product_id_seq OWNED BY supplier_product.id;


--
-- Name: supplier_productcategory; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_productcategory (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    description text NOT NULL,
    image character varying(100)
);


ALTER TABLE public.supplier_productcategory OWNER TO gf_stage;

--
-- Name: supplier_productcategory_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_productcategory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_productcategory_id_seq OWNER TO gf_stage;

--
-- Name: supplier_productcategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_productcategory_id_seq OWNED BY supplier_productcategory.id;


--
-- Name: supplier_productmu; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_productmu (
    id integer NOT NULL,
    name character varying(32) NOT NULL,
    symbol character varying(5) NOT NULL
);


ALTER TABLE public.supplier_productmu OWNER TO gf_stage;

--
-- Name: supplier_productmu_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_productmu_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_productmu_id_seq OWNER TO gf_stage;

--
-- Name: supplier_productmu_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_productmu_id_seq OWNED BY supplier_productmu.id;


--
-- Name: supplier_productpu; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_productpu (
    id integer NOT NULL,
    name character varying(32) NOT NULL,
    symbol character varying(5) NOT NULL,
    description text NOT NULL
);


ALTER TABLE public.supplier_productpu OWNER TO gf_stage;

--
-- Name: supplier_productpu_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_productpu_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_productpu_id_seq OWNER TO gf_stage;

--
-- Name: supplier_productpu_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_productpu_id_seq OWNED BY supplier_productpu.id;


--
-- Name: supplier_supplier; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_supplier (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    seat_id integer,
    vat_number character varying(128),
    ssn character varying(128),
    website character varying(200) NOT NULL,
    frontman_id integer,
    flavour character varying(128) NOT NULL,
    n_employers integer,
    logo character varying(100),
    iban character varying(64) NOT NULL,
    description text NOT NULL,
    CONSTRAINT supplier_supplier_n_employers_check CHECK ((n_employers >= 0))
);


ALTER TABLE public.supplier_supplier OWNER TO gf_stage;

--
-- Name: supplier_supplier_certifications; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_supplier_certifications (
    id integer NOT NULL,
    supplier_id integer NOT NULL,
    certification_id integer NOT NULL
);


ALTER TABLE public.supplier_supplier_certifications OWNER TO gf_stage;

--
-- Name: supplier_supplier_certifications_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_supplier_certifications_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_supplier_certifications_id_seq OWNER TO gf_stage;

--
-- Name: supplier_supplier_certifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_supplier_certifications_id_seq OWNED BY supplier_supplier_certifications.id;


--
-- Name: supplier_supplier_contact_set; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_supplier_contact_set (
    id integer NOT NULL,
    supplier_id integer NOT NULL,
    contact_id integer NOT NULL
);


ALTER TABLE public.supplier_supplier_contact_set OWNER TO gf_stage;

--
-- Name: supplier_supplier_contact_set_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_supplier_contact_set_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_supplier_contact_set_id_seq OWNER TO gf_stage;

--
-- Name: supplier_supplier_contact_set_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_supplier_contact_set_id_seq OWNED BY supplier_supplier_contact_set.id;


--
-- Name: supplier_supplier_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_supplier_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_supplier_id_seq OWNER TO gf_stage;

--
-- Name: supplier_supplier_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_supplier_id_seq OWNED BY supplier_supplier.id;


--
-- Name: supplier_supplieragent; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_supplieragent (
    id integer NOT NULL,
    supplier_id integer NOT NULL,
    person_id integer NOT NULL,
    job_title character varying(256) NOT NULL,
    job_description text NOT NULL
);


ALTER TABLE public.supplier_supplieragent OWNER TO gf_stage;

--
-- Name: supplier_supplieragent_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_supplieragent_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_supplieragent_id_seq OWNER TO gf_stage;

--
-- Name: supplier_supplieragent_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_supplieragent_id_seq OWNED BY supplier_supplieragent.id;


--
-- Name: supplier_supplierconfig; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_supplierconfig (
    id integer NOT NULL,
    supplier_id integer NOT NULL,
    receive_order_via_email_on_finalize boolean NOT NULL,
    use_custom_categories boolean NOT NULL
);


ALTER TABLE public.supplier_supplierconfig OWNER TO gf_stage;

--
-- Name: supplier_supplierconfig_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_supplierconfig_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_supplierconfig_id_seq OWNER TO gf_stage;

--
-- Name: supplier_supplierconfig_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_supplierconfig_id_seq OWNED BY supplier_supplierconfig.id;


--
-- Name: supplier_supplierconfig_products_made_by_set; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_supplierconfig_products_made_by_set (
    id integer NOT NULL,
    supplierconfig_id integer NOT NULL,
    supplier_id integer NOT NULL
);


ALTER TABLE public.supplier_supplierconfig_products_made_by_set OWNER TO gf_stage;

--
-- Name: supplier_supplierconfig_products_made_by_set_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_supplierconfig_products_made_by_set_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_supplierconfig_products_made_by_set_id_seq OWNER TO gf_stage;

--
-- Name: supplier_supplierconfig_products_made_by_set_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_supplierconfig_products_made_by_set_id_seq OWNED BY supplier_supplierconfig_products_made_by_set.id;


--
-- Name: supplier_supplierproductcategory; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_supplierproductcategory (
    id integer NOT NULL,
    supplier_id integer NOT NULL,
    name character varying(128) NOT NULL,
    sorting integer,
    CONSTRAINT supplier_supplierproductcategory_sorting_check CHECK ((sorting >= 0))
);


ALTER TABLE public.supplier_supplierproductcategory OWNER TO gf_stage;

--
-- Name: supplier_supplierproductcategory_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_supplierproductcategory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_supplierproductcategory_id_seq OWNER TO gf_stage;

--
-- Name: supplier_supplierproductcategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_supplierproductcategory_id_seq OWNED BY supplier_supplierproductcategory.id;


--
-- Name: supplier_supplierstock; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_supplierstock (
    id integer NOT NULL,
    supplier_id integer NOT NULL,
    product_id integer NOT NULL,
    supplier_category_id integer,
    image character varying(100),
    price numeric(10,4) NOT NULL,
    code character varying(128),
    amount_available integer NOT NULL,
    units_minimum_amount integer NOT NULL,
    units_per_box numeric(5,2) NOT NULL,
    detail_minimum_amount numeric(5,2),
    detail_step numeric(5,2),
    delivery_notes text NOT NULL,
    deleted boolean NOT NULL,
    CONSTRAINT supplier_supplierstock_amount_available_check CHECK ((amount_available >= 0)),
    CONSTRAINT supplier_supplierstock_units_minimum_amount_check CHECK ((units_minimum_amount >= 0))
);


ALTER TABLE public.supplier_supplierstock OWNER TO gf_stage;

--
-- Name: supplier_supplierstock_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_supplierstock_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_supplierstock_id_seq OWNER TO gf_stage;

--
-- Name: supplier_supplierstock_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_supplierstock_id_seq OWNED BY supplier_supplierstock.id;


--
-- Name: supplier_unitsconversion; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE supplier_unitsconversion (
    id integer NOT NULL,
    src_id integer NOT NULL,
    dst_id integer NOT NULL,
    amount numeric(10,4) NOT NULL
);


ALTER TABLE public.supplier_unitsconversion OWNER TO gf_stage;

--
-- Name: supplier_unitsconversion_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE supplier_unitsconversion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.supplier_unitsconversion_id_seq OWNER TO gf_stage;

--
-- Name: supplier_unitsconversion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE supplier_unitsconversion_id_seq OWNED BY supplier_unitsconversion.id;


--
-- Name: users_userprofile; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE users_userprofile (
    id integer NOT NULL,
    user_id integer NOT NULL,
    default_role_id integer
);


ALTER TABLE public.users_userprofile OWNER TO gf_stage;

--
-- Name: users_userprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE users_userprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_userprofile_id_seq OWNER TO gf_stage;

--
-- Name: users_userprofile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE users_userprofile_id_seq OWNED BY users_userprofile.id;


--
-- Name: workflows_state; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE workflows_state (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    workflow_id integer NOT NULL
);


ALTER TABLE public.workflows_state OWNER TO gf_stage;

--
-- Name: workflows_state_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE workflows_state_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.workflows_state_id_seq OWNER TO gf_stage;

--
-- Name: workflows_state_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE workflows_state_id_seq OWNED BY workflows_state.id;


--
-- Name: workflows_state_transitions; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE workflows_state_transitions (
    id integer NOT NULL,
    state_id integer NOT NULL,
    transition_id integer NOT NULL
);


ALTER TABLE public.workflows_state_transitions OWNER TO gf_stage;

--
-- Name: workflows_state_transitions_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE workflows_state_transitions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.workflows_state_transitions_id_seq OWNER TO gf_stage;

--
-- Name: workflows_state_transitions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE workflows_state_transitions_id_seq OWNED BY workflows_state_transitions.id;


--
-- Name: workflows_stateinheritanceblock; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE workflows_stateinheritanceblock (
    id integer NOT NULL,
    state_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.workflows_stateinheritanceblock OWNER TO gf_stage;

--
-- Name: workflows_stateinheritanceblock_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE workflows_stateinheritanceblock_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.workflows_stateinheritanceblock_id_seq OWNER TO gf_stage;

--
-- Name: workflows_stateinheritanceblock_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE workflows_stateinheritanceblock_id_seq OWNED BY workflows_stateinheritanceblock.id;


--
-- Name: workflows_stateobjectrelation; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE workflows_stateobjectrelation (
    id integer NOT NULL,
    content_type_id integer,
    content_id integer,
    state_id integer NOT NULL,
    CONSTRAINT workflows_stateobjectrelation_content_id_check CHECK ((content_id >= 0))
);


ALTER TABLE public.workflows_stateobjectrelation OWNER TO gf_stage;

--
-- Name: workflows_stateobjectrelation_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE workflows_stateobjectrelation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.workflows_stateobjectrelation_id_seq OWNER TO gf_stage;

--
-- Name: workflows_stateobjectrelation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE workflows_stateobjectrelation_id_seq OWNED BY workflows_stateobjectrelation.id;


--
-- Name: workflows_statepermissionrelation; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE workflows_statepermissionrelation (
    id integer NOT NULL,
    state_id integer NOT NULL,
    permission_id integer NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE public.workflows_statepermissionrelation OWNER TO gf_stage;

--
-- Name: workflows_statepermissionrelation_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE workflows_statepermissionrelation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.workflows_statepermissionrelation_id_seq OWNER TO gf_stage;

--
-- Name: workflows_statepermissionrelation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE workflows_statepermissionrelation_id_seq OWNED BY workflows_statepermissionrelation.id;


--
-- Name: workflows_transition; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE workflows_transition (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    workflow_id integer NOT NULL,
    destination_id integer,
    condition character varying(100) NOT NULL,
    permission_id integer
);


ALTER TABLE public.workflows_transition OWNER TO gf_stage;

--
-- Name: workflows_transition_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE workflows_transition_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.workflows_transition_id_seq OWNER TO gf_stage;

--
-- Name: workflows_transition_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE workflows_transition_id_seq OWNED BY workflows_transition.id;


--
-- Name: workflows_workflow; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE workflows_workflow (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    initial_state_id integer
);


ALTER TABLE public.workflows_workflow OWNER TO gf_stage;

--
-- Name: workflows_workflow_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE workflows_workflow_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.workflows_workflow_id_seq OWNER TO gf_stage;

--
-- Name: workflows_workflow_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE workflows_workflow_id_seq OWNED BY workflows_workflow.id;


--
-- Name: workflows_workflowmodelrelation; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE workflows_workflowmodelrelation (
    id integer NOT NULL,
    content_type_id integer NOT NULL,
    workflow_id integer NOT NULL
);


ALTER TABLE public.workflows_workflowmodelrelation OWNER TO gf_stage;

--
-- Name: workflows_workflowmodelrelation_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE workflows_workflowmodelrelation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.workflows_workflowmodelrelation_id_seq OWNER TO gf_stage;

--
-- Name: workflows_workflowmodelrelation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE workflows_workflowmodelrelation_id_seq OWNED BY workflows_workflowmodelrelation.id;


--
-- Name: workflows_workflowobjectrelation; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE workflows_workflowobjectrelation (
    id integer NOT NULL,
    content_type_id integer,
    content_id integer,
    workflow_id integer NOT NULL,
    CONSTRAINT workflows_workflowobjectrelation_content_id_check CHECK ((content_id >= 0))
);


ALTER TABLE public.workflows_workflowobjectrelation OWNER TO gf_stage;

--
-- Name: workflows_workflowobjectrelation_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE workflows_workflowobjectrelation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.workflows_workflowobjectrelation_id_seq OWNER TO gf_stage;

--
-- Name: workflows_workflowobjectrelation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE workflows_workflowobjectrelation_id_seq OWNED BY workflows_workflowobjectrelation.id;


--
-- Name: workflows_workflowpermissionrelation; Type: TABLE; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE TABLE workflows_workflowpermissionrelation (
    id integer NOT NULL,
    workflow_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.workflows_workflowpermissionrelation OWNER TO gf_stage;

--
-- Name: workflows_workflowpermissionrelation_id_seq; Type: SEQUENCE; Schema: public; Owner: gf_stage
--

CREATE SEQUENCE workflows_workflowpermissionrelation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.workflows_workflowpermissionrelation_id_seq OWNER TO gf_stage;

--
-- Name: workflows_workflowpermissionrelation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: gf_stage
--

ALTER SEQUENCE workflows_workflowpermissionrelation_id_seq OWNED BY workflows_workflowpermissionrelation.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY auth_message ALTER COLUMN id SET DEFAULT nextval('auth_message_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_contact ALTER COLUMN id SET DEFAULT nextval('base_contact_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_defaulttransition ALTER COLUMN id SET DEFAULT nextval('base_defaulttransition_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_historicalcontact ALTER COLUMN history_id SET DEFAULT nextval('base_historicalcontact_history_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_historicaldefaulttransition ALTER COLUMN history_id SET DEFAULT nextval('base_historicaldefaulttransition_history_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_historicalperson ALTER COLUMN history_id SET DEFAULT nextval('base_historicalperson_history_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_historicalplace ALTER COLUMN history_id SET DEFAULT nextval('base_historicalplace_history_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_person ALTER COLUMN id SET DEFAULT nextval('base_person_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_person_contact_set ALTER COLUMN id SET DEFAULT nextval('base_person_contact_set_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_place ALTER COLUMN id SET DEFAULT nextval('base_place_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY blockconfiguration ALTER COLUMN id SET DEFAULT nextval('blockconfiguration_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY captcha_captchastore ALTER COLUMN id SET DEFAULT nextval('captcha_captchastore_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY des_des_info_people_set ALTER COLUMN id SET DEFAULT nextval('des_des_info_people_set_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY des_siteattr ALTER COLUMN id SET DEFAULT nextval('des_siteattr_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY django_comment_flags ALTER COLUMN id SET DEFAULT nextval('django_comment_flags_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY django_comments ALTER COLUMN id SET DEFAULT nextval('django_comments_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY django_site ALTER COLUMN id SET DEFAULT nextval('django_site_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY flexi_auth_param ALTER COLUMN id SET DEFAULT nextval('flexi_auth_param_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY flexi_auth_paramrole ALTER COLUMN id SET DEFAULT nextval('flexi_auth_paramrole_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY flexi_auth_paramrole_param_set ALTER COLUMN id SET DEFAULT nextval('flexi_auth_paramrole_param_set_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY flexi_auth_principalparamrolerelation ALTER COLUMN id SET DEFAULT nextval('flexi_auth_principalparamrolerelation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_delivery ALTER COLUMN id SET DEFAULT nextval('gas_delivery_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gas ALTER COLUMN id SET DEFAULT nextval('gas_gas_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gas_contact_set ALTER COLUMN id SET DEFAULT nextval('gas_gas_contact_set_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasactivist ALTER COLUMN id SET DEFAULT nextval('gas_gasactivist_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasconfig ALTER COLUMN id SET DEFAULT nextval('gas_gasconfig_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasconfig_intergas_connection_set ALTER COLUMN id SET DEFAULT nextval('gas_gasconfig_intergas_connection_set_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasmember ALTER COLUMN id SET DEFAULT nextval('gas_gasmember_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasmember_available_for_roles ALTER COLUMN id SET DEFAULT nextval('gas_gasmember_available_for_roles_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasmemberorder ALTER COLUMN id SET DEFAULT nextval('gas_gasmemberorder_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gassupplierorder ALTER COLUMN id SET DEFAULT nextval('gas_gassupplierorder_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gassupplierorderproduct ALTER COLUMN id SET DEFAULT nextval('gas_gassupplierorderproduct_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gassuppliersolidalpact ALTER COLUMN id SET DEFAULT nextval('gas_gassuppliersolidalpact_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gassupplierstock ALTER COLUMN id SET DEFAULT nextval('gas_gassupplierstock_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicaldelivery ALTER COLUMN history_id SET DEFAULT nextval('gas_historicaldelivery_history_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicalgas ALTER COLUMN history_id SET DEFAULT nextval('gas_historicalgas_history_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicalgasactivist ALTER COLUMN history_id SET DEFAULT nextval('gas_historicalgasactivist_history_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicalgasconfig ALTER COLUMN history_id SET DEFAULT nextval('gas_historicalgasconfig_history_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicalgasmember ALTER COLUMN history_id SET DEFAULT nextval('gas_historicalgasmember_history_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicalgasmemberorder ALTER COLUMN history_id SET DEFAULT nextval('gas_historicalgasmemberorder_history_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicalgassupplierorder ALTER COLUMN history_id SET DEFAULT nextval('gas_historicalgassupplierorder_history_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicalgassupplierorderproduct ALTER COLUMN history_id SET DEFAULT nextval('gas_historicalgassupplierorderproduct_history_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicalgassuppliersolidalpact ALTER COLUMN history_id SET DEFAULT nextval('gas_historicalgassuppliersolidalpact_history_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicalgassupplierstock ALTER COLUMN history_id SET DEFAULT nextval('gas_historicalgassupplierstock_history_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicalwithdrawal ALTER COLUMN history_id SET DEFAULT nextval('gas_historicalwithdrawal_history_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_withdrawal ALTER COLUMN id SET DEFAULT nextval('gas_withdrawal_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY notification_notice ALTER COLUMN id SET DEFAULT nextval('notification_notice_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY notification_noticequeuebatch ALTER COLUMN id SET DEFAULT nextval('notification_noticequeuebatch_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY notification_noticesetting ALTER COLUMN id SET DEFAULT nextval('notification_noticesetting_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY notification_noticetype ALTER COLUMN id SET DEFAULT nextval('notification_noticetype_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY notification_observeditem ALTER COLUMN id SET DEFAULT nextval('notification_observeditem_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY permissions_objectpermission ALTER COLUMN id SET DEFAULT nextval('permissions_objectpermission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY permissions_objectpermissioninheritanceblock ALTER COLUMN id SET DEFAULT nextval('permissions_objectpermissioninheritanceblock_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY permissions_permission ALTER COLUMN id SET DEFAULT nextval('permissions_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY permissions_permission_content_types ALTER COLUMN id SET DEFAULT nextval('permissions_permission_content_types_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY permissions_principalrolerelation ALTER COLUMN id SET DEFAULT nextval('permissions_principalrolerelation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY permissions_role ALTER COLUMN id SET DEFAULT nextval('permissions_role_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY registration_registrationprofile ALTER COLUMN id SET DEFAULT nextval('registration_registrationprofile_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY rest_homepage ALTER COLUMN id SET DEFAULT nextval('rest_homepage_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY rest_page ALTER COLUMN id SET DEFAULT nextval('rest_page_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_account ALTER COLUMN id SET DEFAULT nextval('simple_accounting_account_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_accountsystem ALTER COLUMN id SET DEFAULT nextval('simple_accounting_accountsystem_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_accounttype ALTER COLUMN id SET DEFAULT nextval('simple_accounting_accounttype_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_cashflow ALTER COLUMN id SET DEFAULT nextval('simple_accounting_cashflow_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_invoice ALTER COLUMN id SET DEFAULT nextval('simple_accounting_invoice_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_ledgerentry ALTER COLUMN id SET DEFAULT nextval('simple_accounting_ledgerentry_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_split ALTER COLUMN id SET DEFAULT nextval('simple_accounting_split_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_subject ALTER COLUMN id SET DEFAULT nextval('simple_accounting_subject_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_transaction ALTER COLUMN id SET DEFAULT nextval('simple_accounting_transaction_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_transaction_split_set ALTER COLUMN id SET DEFAULT nextval('simple_accounting_transaction_split_set_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_transactionreference ALTER COLUMN id SET DEFAULT nextval('simple_accounting_transactionreference_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY south_migrationhistory ALTER COLUMN id SET DEFAULT nextval('south_migrationhistory_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_certification ALTER COLUMN id SET DEFAULT nextval('supplier_certification_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalcertification ALTER COLUMN history_id SET DEFAULT nextval('supplier_historicalcertification_history_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalproduct ALTER COLUMN history_id SET DEFAULT nextval('supplier_historicalproduct_history_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalproductcategory ALTER COLUMN history_id SET DEFAULT nextval('supplier_historicalproductcategory_history_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalproductmu ALTER COLUMN history_id SET DEFAULT nextval('supplier_historicalproductmu_history_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalproductpu ALTER COLUMN history_id SET DEFAULT nextval('supplier_historicalproductpu_history_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalsupplier ALTER COLUMN history_id SET DEFAULT nextval('supplier_historicalsupplier_history_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalsupplieragent ALTER COLUMN history_id SET DEFAULT nextval('supplier_historicalsupplieragent_history_id_seq'::regclass);


--
-- Name: history_id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalsupplierstock ALTER COLUMN history_id SET DEFAULT nextval('supplier_historicalsupplierstock_history_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_product ALTER COLUMN id SET DEFAULT nextval('supplier_product_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_productcategory ALTER COLUMN id SET DEFAULT nextval('supplier_productcategory_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_productmu ALTER COLUMN id SET DEFAULT nextval('supplier_productmu_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_productpu ALTER COLUMN id SET DEFAULT nextval('supplier_productpu_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplier ALTER COLUMN id SET DEFAULT nextval('supplier_supplier_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplier_certifications ALTER COLUMN id SET DEFAULT nextval('supplier_supplier_certifications_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplier_contact_set ALTER COLUMN id SET DEFAULT nextval('supplier_supplier_contact_set_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplieragent ALTER COLUMN id SET DEFAULT nextval('supplier_supplieragent_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplierconfig ALTER COLUMN id SET DEFAULT nextval('supplier_supplierconfig_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplierconfig_products_made_by_set ALTER COLUMN id SET DEFAULT nextval('supplier_supplierconfig_products_made_by_set_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplierproductcategory ALTER COLUMN id SET DEFAULT nextval('supplier_supplierproductcategory_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplierstock ALTER COLUMN id SET DEFAULT nextval('supplier_supplierstock_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_unitsconversion ALTER COLUMN id SET DEFAULT nextval('supplier_unitsconversion_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY users_userprofile ALTER COLUMN id SET DEFAULT nextval('users_userprofile_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_state ALTER COLUMN id SET DEFAULT nextval('workflows_state_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_state_transitions ALTER COLUMN id SET DEFAULT nextval('workflows_state_transitions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_stateinheritanceblock ALTER COLUMN id SET DEFAULT nextval('workflows_stateinheritanceblock_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_stateobjectrelation ALTER COLUMN id SET DEFAULT nextval('workflows_stateobjectrelation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_statepermissionrelation ALTER COLUMN id SET DEFAULT nextval('workflows_statepermissionrelation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_transition ALTER COLUMN id SET DEFAULT nextval('workflows_transition_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_workflow ALTER COLUMN id SET DEFAULT nextval('workflows_workflow_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_workflowmodelrelation ALTER COLUMN id SET DEFAULT nextval('workflows_workflowmodelrelation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_workflowobjectrelation ALTER COLUMN id SET DEFAULT nextval('workflows_workflowobjectrelation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_workflowpermissionrelation ALTER COLUMN id SET DEFAULT nextval('workflows_workflowpermissionrelation_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY auth_group (id, name) FROM stdin;
4	gasmembers
3	gas_referrer_suppliers
2	suppliers
1	techs
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('auth_group_id_seq', 4, true);


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
67	4	86
68	4	91
69	4	92
70	4	97
71	4	98
72	3	160
73	3	97
74	3	98
75	3	162
76	3	161
77	3	109
78	3	110
79	3	113
80	3	86
81	3	151
82	3	152
83	3	153
84	3	91
85	3	92
86	3	157
87	3	158
88	3	159
89	2	160
90	2	97
91	2	98
92	2	161
93	2	162
94	2	110
95	2	113
96	2	86
97	2	151
98	2	152
99	2	153
100	2	91
101	2	92
102	2	157
103	2	158
104	2	159
105	1	130
106	1	131
107	1	132
108	1	151
109	1	152
110	1	153
111	1	157
112	1	158
113	1	159
114	1	160
115	1	161
116	1	162
117	1	178
118	1	179
119	1	86
120	1	87
121	1	91
122	1	92
123	1	93
124	1	97
125	1	98
126	1	99
127	1	234
128	1	109
129	1	110
130	1	240
131	1	113
132	1	251
133	1	252
134	1	253
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 134, true);


--
-- Data for Name: auth_message; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY auth_message (id, user_id, message) FROM stdin;
\.


--
-- Name: auth_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('auth_message_id_seq', 1, false);


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add permission	1	add_permission
2	Can change permission	1	change_permission
3	Can delete permission	1	delete_permission
4	Can add object permission	2	add_objectpermission
5	Can change object permission	2	change_objectpermission
6	Can delete object permission	2	delete_objectpermission
7	Can add object permission inheritance block	3	add_objectpermissioninheritanceblock
8	Can change object permission inheritance block	3	change_objectpermissioninheritanceblock
9	Can delete object permission inheritance block	3	delete_objectpermissioninheritanceblock
10	Can add role	4	add_role
11	Can change role	4	change_role
12	Can delete role	4	delete_role
13	Can add principal role relation	5	add_principalrolerelation
14	Can change principal role relation	5	change_principalrolerelation
15	Can delete principal role relation	5	delete_principalrolerelation
16	Can add workflow	6	add_workflow
17	Can change workflow	6	change_workflow
18	Can delete workflow	6	delete_workflow
19	Can add state	7	add_state
20	Can change state	7	change_state
21	Can delete state	7	delete_state
22	Can add transition	8	add_transition
23	Can change transition	8	change_transition
24	Can delete transition	8	delete_transition
25	Can add state object relation	9	add_stateobjectrelation
26	Can change state object relation	9	change_stateobjectrelation
27	Can delete state object relation	9	delete_stateobjectrelation
28	Can add workflow object relation	10	add_workflowobjectrelation
29	Can change workflow object relation	10	change_workflowobjectrelation
30	Can delete workflow object relation	10	delete_workflowobjectrelation
31	Can add workflow model relation	11	add_workflowmodelrelation
32	Can change workflow model relation	11	change_workflowmodelrelation
33	Can delete workflow model relation	11	delete_workflowmodelrelation
34	Can add workflow permission relation	12	add_workflowpermissionrelation
35	Can change workflow permission relation	12	change_workflowpermissionrelation
36	Can delete workflow permission relation	12	delete_workflowpermissionrelation
37	Can add state inheritance block	13	add_stateinheritanceblock
38	Can change state inheritance block	13	change_stateinheritanceblock
39	Can delete state inheritance block	13	delete_stateinheritanceblock
40	Can add state permission relation	14	add_statepermissionrelation
41	Can change state permission relation	14	change_statepermissionrelation
42	Can delete state permission relation	14	delete_statepermissionrelation
43	Can add Parameter	15	add_param
44	Can change Parameter	15	change_param
45	Can delete Parameter	15	delete_param
46	Can add Parametric Role	16	add_paramrole
47	Can change Parametric Role	16	change_paramrole
48	Can delete Parametric Role	16	delete_paramrole
49	Can add principal param role relation	17	add_principalparamrolerelation
50	Can change principal param role relation	17	change_principalparamrolerelation
51	Can delete principal param role relation	17	delete_principalparamrolerelation
52	Can add subject	18	add_subject
53	Can change subject	18	change_subject
54	Can delete subject	18	delete_subject
55	Can add account type	19	add_accounttype
56	Can change account type	19	change_accounttype
57	Can delete account type	19	delete_accounttype
58	Can add account system	20	add_accountsystem
59	Can change account system	20	change_accountsystem
60	Can delete account system	20	delete_accountsystem
61	Can add account	21	add_account
62	Can change account	21	change_account
63	Can delete account	21	delete_account
64	Can add cash flow	22	add_cashflow
65	Can change cash flow	22	change_cashflow
66	Can delete cash flow	22	delete_cashflow
67	Can add split	23	add_split
68	Can change split	23	change_split
69	Can delete split	23	delete_split
70	Can add transaction	24	add_transaction
71	Can change transaction	24	change_transaction
72	Can delete transaction	24	delete_transaction
73	Can add transaction reference	25	add_transactionreference
74	Can change transaction reference	25	change_transactionreference
75	Can delete transaction reference	25	delete_transactionreference
76	Can add ledger entry	26	add_ledgerentry
77	Can change ledger entry	26	change_ledgerentry
78	Can delete ledger entry	26	delete_ledgerentry
79	Can add invoice	27	add_invoice
80	Can change invoice	27	change_invoice
81	Can delete invoice	27	delete_invoice
82	Can add historical person	28	add_historicalperson
83	Can change historical person	28	change_historicalperson
84	Can delete historical person	28	delete_historicalperson
85	Can add person	29	add_person
86	Can change person	29	change_person
87	Can delete person	29	delete_person
88	Can add historical contact	30	add_historicalcontact
89	Can change historical contact	30	change_historicalcontact
90	Can delete historical contact	30	delete_historicalcontact
91	Can add contact	31	add_contact
92	Can change contact	31	change_contact
93	Can delete contact	31	delete_contact
94	Can add historical place	32	add_historicalplace
95	Can change historical place	32	change_historicalplace
96	Can delete historical place	32	delete_historicalplace
97	Can add place	33	add_place
98	Can change place	33	change_place
99	Can delete place	33	delete_place
100	Can add historical default transition	34	add_historicaldefaulttransition
101	Can change historical default transition	34	change_historicaldefaulttransition
102	Can delete historical default transition	34	delete_historicaldefaulttransition
103	Can add default transition	35	add_defaulttransition
104	Can change default transition	35	change_defaulttransition
105	Can delete default transition	35	delete_defaulttransition
106	Can add historical supplier	36	add_historicalsupplier
107	Can change historical supplier	36	change_historicalsupplier
108	Can delete historical supplier	36	delete_historicalsupplier
109	Can add supplier	37	add_supplier
110	Can change supplier	37	change_supplier
111	Can delete supplier	37	delete_supplier
112	Can add supplier config	38	add_supplierconfig
113	Can change supplier config	38	change_supplierconfig
114	Can delete supplier config	38	delete_supplierconfig
115	Can add historical supplier agent	39	add_historicalsupplieragent
116	Can change historical supplier agent	39	change_historicalsupplieragent
117	Can delete historical supplier agent	39	delete_historicalsupplieragent
118	Can add supplier agent	40	add_supplieragent
119	Can change supplier agent	40	change_supplieragent
120	Can delete supplier agent	40	delete_supplieragent
121	Can add historical certification	41	add_historicalcertification
122	Can change historical certification	41	change_historicalcertification
123	Can delete historical certification	41	delete_historicalcertification
124	Can add certification	42	add_certification
125	Can change certification	42	change_certification
126	Can delete certification	42	delete_certification
127	Can add historical product category	43	add_historicalproductcategory
128	Can change historical product category	43	change_historicalproductcategory
129	Can delete historical product category	43	delete_historicalproductcategory
130	Can add Product category	44	add_productcategory
131	Can change Product category	44	change_productcategory
132	Can delete Product category	44	delete_productcategory
133	Can add historical product mu	45	add_historicalproductmu
134	Can change historical product mu	45	change_historicalproductmu
135	Can delete historical product mu	45	delete_historicalproductmu
136	Can add measure unit	46	add_productmu
137	Can change measure unit	46	change_productmu
138	Can delete measure unit	46	delete_productmu
139	Can add historical product pu	47	add_historicalproductpu
140	Can change historical product pu	47	change_historicalproductpu
141	Can delete historical product pu	47	delete_historicalproductpu
142	Can add product unit	48	add_productpu
143	Can change product unit	48	change_productpu
144	Can delete product unit	48	delete_productpu
145	Can add units conversion	49	add_unitsconversion
146	Can change units conversion	49	change_unitsconversion
147	Can delete units conversion	49	delete_unitsconversion
148	Can add historical product	50	add_historicalproduct
149	Can change historical product	50	change_historicalproduct
150	Can delete historical product	50	delete_historicalproduct
151	Can add product	51	add_product
152	Can change product	51	change_product
153	Can delete product	51	delete_product
154	Can add historical supplier stock	52	add_historicalsupplierstock
155	Can change historical supplier stock	52	change_historicalsupplierstock
156	Can delete historical supplier stock	52	delete_historicalsupplierstock
157	Can add supplier stock	53	add_supplierstock
158	Can change supplier stock	53	change_supplierstock
159	Can delete supplier stock	53	delete_supplierstock
160	Can add supplier product category	54	add_supplierproductcategory
161	Can change supplier product category	54	change_supplierproductcategory
162	Can delete supplier product category	54	delete_supplierproductcategory
163	Can add Block configuration data	55	add_blockconfiguration
164	Can change Block configuration data	55	change_blockconfiguration
165	Can delete Block configuration data	55	delete_blockconfiguration
166	Can add page	56	add_page
167	Can change page	56	change_page
168	Can delete page	56	delete_page
169	Can add home page	57	add_homepage
170	Can change home page	57	change_homepage
171	Can delete home page	57	delete_homepage
172	Can add permission	58	add_permission
173	Can change permission	58	change_permission
174	Can delete permission	58	delete_permission
175	Can add group	59	add_group
176	Can change group	59	change_group
177	Can delete group	59	delete_group
178	Can add user	60	add_user
179	Can change user	60	change_user
180	Can delete user	60	delete_user
181	Can add message	61	add_message
182	Can change message	61	change_message
183	Can delete message	61	delete_message
184	Can add content type	62	add_contenttype
185	Can change content type	62	change_contenttype
186	Can delete content type	62	delete_contenttype
187	Can add session	63	add_session
188	Can change session	63	change_session
189	Can delete session	63	delete_session
190	Can add site	64	add_site
191	Can change site	64	change_site
192	Can delete site	64	delete_site
193	Can add site	65	add_des
194	Can change site	65	change_des
195	Can delete site	65	delete_des
196	Can add environment variable	66	add_siteattr
197	Can change environment variable	66	change_siteattr
198	Can delete environment variable	66	delete_siteattr
199	Can add log entry	67	add_logentry
200	Can change log entry	67	change_logentry
201	Can delete log entry	67	delete_logentry
202	Can add comment	68	add_comment
203	Can change comment	68	change_comment
204	Can delete comment	68	delete_comment
205	Can moderate comments	68	can_moderate
206	Can add comment flag	69	add_commentflag
207	Can change comment flag	69	change_commentflag
208	Can delete comment flag	69	delete_commentflag
209	Can add notice type	70	add_noticetype
210	Can change notice type	70	change_noticetype
211	Can delete notice type	70	delete_noticetype
212	Can add notice setting	71	add_noticesetting
213	Can change notice setting	71	change_noticesetting
214	Can delete notice setting	71	delete_noticesetting
215	Can add notice	72	add_notice
216	Can change notice	72	change_notice
217	Can delete notice	72	delete_notice
218	Can add notice queue batch	73	add_noticequeuebatch
219	Can change notice queue batch	73	change_noticequeuebatch
220	Can delete notice queue batch	73	delete_noticequeuebatch
221	Can add observed item	74	add_observeditem
222	Can change observed item	74	change_observeditem
223	Can delete observed item	74	delete_observeditem
224	Can add registration profile	75	add_registrationprofile
225	Can change registration profile	75	change_registrationprofile
226	Can delete registration profile	75	delete_registrationprofile
227	Can add migration history	76	add_migrationhistory
228	Can change migration history	76	change_migrationhistory
229	Can delete migration history	76	delete_migrationhistory
230	Can add historical gas	77	add_historicalgas
231	Can change historical gas	77	change_historicalgas
232	Can delete historical gas	77	delete_historicalgas
233	Can add gas	78	add_gas
234	Can change gas	78	change_gas
235	Can delete gas	78	delete_gas
236	Can add historical gas config	79	add_historicalgasconfig
237	Can change historical gas config	79	change_historicalgasconfig
238	Can delete historical gas config	79	delete_historicalgasconfig
239	Can add GAS options	80	add_gasconfig
240	Can change GAS options	80	change_gasconfig
241	Can delete GAS options	80	delete_gasconfig
242	Can add historical gas activist	81	add_historicalgasactivist
243	Can change historical gas activist	81	change_historicalgasactivist
244	Can delete historical gas activist	81	delete_historicalgasactivist
245	Can add GAS activist	82	add_gasactivist
246	Can change GAS activist	82	change_gasactivist
247	Can delete GAS activist	82	delete_gasactivist
248	Can add historical gas member	83	add_historicalgasmember
249	Can change historical gas member	83	change_historicalgasmember
250	Can delete historical gas member	83	delete_historicalgasmember
251	Can add GAS member	84	add_gasmember
252	Can change GAS member	84	change_gasmember
253	Can delete GAS member	84	delete_gasmember
254	Can add historical gas supplier stock	85	add_historicalgassupplierstock
255	Can change historical gas supplier stock	85	change_historicalgassupplierstock
256	Can delete historical gas supplier stock	85	delete_historicalgassupplierstock
257	Can add GAS supplier stock	86	add_gassupplierstock
258	Can change GAS supplier stock	86	change_gassupplierstock
259	Can delete GAS supplier stock	86	delete_gassupplierstock
260	Can add historical gas supplier solidal pact	87	add_historicalgassuppliersolidalpact
261	Can change historical gas supplier solidal pact	87	change_historicalgassuppliersolidalpact
262	Can delete historical gas supplier solidal pact	87	delete_historicalgassuppliersolidalpact
263	Can add gas supplier solidal pact	88	add_gassuppliersolidalpact
264	Can change gas supplier solidal pact	88	change_gassuppliersolidalpact
265	Can delete gas supplier solidal pact	88	delete_gassuppliersolidalpact
266	Can add historical gas supplier order	89	add_historicalgassupplierorder
267	Can change historical gas supplier order	89	change_historicalgassupplierorder
268	Can delete historical gas supplier order	89	delete_historicalgassupplierorder
269	Can add order issued to supplier	90	add_gassupplierorder
270	Can change order issued to supplier	90	change_gassupplierorder
271	Can delete order issued to supplier	90	delete_gassupplierorder
272	Can add historical gas supplier order product	91	add_historicalgassupplierorderproduct
273	Can change historical gas supplier order product	91	change_historicalgassupplierorderproduct
274	Can delete historical gas supplier order product	91	delete_historicalgassupplierorderproduct
275	Can add gas supplier order product	92	add_gassupplierorderproduct
276	Can change gas supplier order product	92	change_gassupplierorderproduct
277	Can delete gas supplier order product	92	delete_gassupplierorderproduct
278	Can add historical gas member order	93	add_historicalgasmemberorder
279	Can change historical gas member order	93	change_historicalgasmemberorder
280	Can delete historical gas member order	93	delete_historicalgasmemberorder
281	Can add GAS member order	94	add_gasmemberorder
282	Can change GAS member order	94	change_gasmemberorder
283	Can delete GAS member order	94	delete_gasmemberorder
284	Can add historical delivery	95	add_historicaldelivery
285	Can change historical delivery	95	change_historicaldelivery
286	Can delete historical delivery	95	delete_historicaldelivery
287	Can add delivery	96	add_delivery
288	Can change delivery	96	change_delivery
289	Can delete delivery	96	delete_delivery
290	Can add historical withdrawal	97	add_historicalwithdrawal
291	Can change historical withdrawal	97	change_historicalwithdrawal
292	Can delete historical withdrawal	97	delete_historicalwithdrawal
293	Can add wihtdrawal	98	add_withdrawal
294	Can change wihtdrawal	98	change_withdrawal
295	Can delete wihtdrawal	98	delete_withdrawal
296	Can add user profile	99	add_userprofile
297	Can change user profile	99	change_userprofile
298	Can delete user profile	99	delete_userprofile
299	Can add captcha store	100	add_captchastore
300	Can change captcha store	100	change_captchastore
301	Can delete captcha store	100	delete_captchastore
\.


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('auth_permission_id_seq', 301, true);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY auth_user (id, username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined) FROM stdin;
32	gasper01	Gasper	01	gasper01@test.com	sha1$4eb97$068a55e55567c05cb716595481f7150ec0d8a96a	t	t	f	2014-03-18 20:36:39.906894+01	2014-03-18 20:29:56.709591+01
33	gasper02	Gasper	02	gasper02@test.com	sha1$eb74f$4d5e24b6f47e9845787e1fd64d1d496a6d1193d4	t	t	f	2014-03-18 20:37:05.848136+01	2014-03-18 20:31:23.507223+01
21	fintaregistrazione	IL Finto	finto	dev@gasistafelice.org	sha1$537c9$35c4f674714d095de5fb1097ffa96783a36a3d4d	t	f	f	2014-02-20 00:33:21.960874+01	2014-02-20 00:33:21.960874+01
34	utente	utente	generico	utente@test.org	sha1$a4272$3de05ebf4133cdac126aade8cdce9ced660e5aed	t	t	f	2014-05-07 22:10:53.287213+02	2014-05-07 20:52:46.174515+02
36	fornitore01	forni	tore	fornitore@example.org	sha1$b244a$a4be012f5383f6442698db4bcb4a807b936c7b36	t	t	f	2015-02-03 10:09:58+01	2015-02-02 13:16:49+01
18	kobe	a	a	kobebryan@example.org	sha1$62abc$fc54e6e93896bc91173050af422365942a7140e7	t	t	f	2014-02-17 19:36:06+01	2014-02-17 19:36:06+01
22	luca	Luca		elferodelfero@example.org	sha1$ffe27$466d3a2db93b71392b5697fc96ed0117de9e2201	t	f	f	2014-02-20 16:23:16+01	2014-02-20 16:23:16+01
16	orly	Orlando		orlypiuchepuoi@example.org	sha1$5e531$b42001015821a66e1e543cdc51c9dd5fb8500bd7	t	t	f	2014-02-27 17:18:49+01	2014-02-17 00:23:10+01
3	02gas1	Gasista_02	DelGas_01	gasista02@gas01.test	sha1$44841$7cdc271ee203ecf8c59fd36819a9eb428e191056	t	t	f	2014-02-08 03:52:41.595553+01	2014-01-19 15:25:33+01
23	orly1	Agente_	speciale Orly1	agentespecialeorly@example.org	sha1$a1f68$0812f4c2a59188b29010de2d4b1814db7307eea4	t	t	f	2014-02-27 16:58:58+01	2014-02-27 16:48:55+01
37	refecon01	Refe	Rente	referenteeconomico@example.org	sha1$07cf2$642aae7039af7b56d9e4e9cd973b8d0d3bdb94e7	t	t	f	2015-02-04 08:55:17+01	2015-02-02 13:29:10+01
20	riprovo	Riprovo	Ioriprovo	ciriprovo@example.org	sha1$602a6$ef3472995b3078bca7ff8a0db4c33b9be1233f38	t	t	f	2014-02-20 17:31:20+01	2014-02-20 00:30:25+01
5	01gas2	Gasista_01	DelGas_02	gasista01@gas02.test	sha1$642f5$3b07a3fc354d7c490561d9ee4142c580dca3f699	t	t	f	2014-11-04 16:07:29.651626+01	2014-01-19 15:33:17+01
1	admin	Referente informatico	del Test-Des	wargames@example.org	sha1$0f36c$259673a51941e7c00a83992ad60fe8dc45cb4e40	t	t	t	2015-03-02 01:01:25.473297+01	2014-01-18 02:20:14+01
4	02gas2	Gasista_02	DelGas_02	gasista02@gas02.test	sha1$f6022$e49e7c06f6f80af978d00476aa91a78418b6fee6	t	t	f	2014-11-04 16:08:48.818095+01	2014-01-19 15:31:50+01
2	01gas1	Gasista_01	DelGas_01	gasista01@gas01.test	sha1$7f314$3bb342d46a624e1b479776948ec090a9414729e7	t	t	f	2015-02-03 10:02:40.384927+01	2014-01-19 14:54:46+01
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
6	5	4
7	2	4
8	3	4
9	4	4
10	2	1
11	5	3
12	4	3
13	2	3
14	3	3
16	4	1
35	21	4
55	32	4
56	33	4
60	34	4
64	36	2
65	18	3
66	18	4
67	22	2
68	16	2
69	16	3
70	16	4
71	23	2
72	37	4
73	20	3
74	20	4
\.


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 74, true);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('auth_user_id_seq', 37, true);


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Data for Name: base_contact; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY base_contact (id, flavour, value, is_preferred, description) FROM stdin;
2	EMAIL	gasista01@gas01.test	f	
4	EMAIL	gasista02@gas01.test	f	
5	EMAIL	gas02@test.test	t	
6	EMAIL	gasista02@gas02.test	f	
12	PHONE	3333333333	f	
3	PHONE	123456789	t	
7	EMAIL	gasista01@gas02.test	f	
14	EMAIL	testmontecassiano@test.org	t	
18	PHONE	2332132	f	
41	PHONE	12345678	f	
43	PHONE	123123123123	f	
44	PHONE	12141234	f	
46	PHONE	123123123	f	
1	EMAIL	gas01@test.org	t	
51	EMAIL	generico@ciao.it	t	
52	PHONE	123456789	t	
53	EMAIL	miamail@ciao.it	t	
54	PHONE	289340829	t	
62	PHONE	00000000	f	
68	EMAIL	gasper01@test.com	f	
69	EMAIL	gasper02@test.com	f	
70	PHONE	000000	f	
49	PHONE	0000000	t	
72	EMAIL	utente@test.org	f	
73	PHONE	000000000	f	
38	PHONE	0	t	
\.


--
-- Name: base_contact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('base_contact_id_seq', 77, true);


--
-- Data for Name: base_defaulttransition; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY base_defaulttransition (id, workflow_id, state_id, transition_id) FROM stdin;
1	3	15	16
2	3	16	18
3	3	17	19
4	3	18	20
5	3	19	21
\.


--
-- Name: base_defaulttransition_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('base_defaulttransition_id_seq', 5, true);


--
-- Data for Name: base_historicalcontact; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY base_historicalcontact (id, flavour, value, is_preferred, description, history_id, history_date, history_user_id, history_type) FROM stdin;
\.


--
-- Name: base_historicalcontact_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('base_historicalcontact_history_id_seq', 138, true);


--
-- Data for Name: base_historicaldefaulttransition; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY base_historicaldefaulttransition (id, workflow_id, state_id, transition_id, history_id, history_date, history_user_id, history_type) FROM stdin;
\.


--
-- Name: base_historicaldefaulttransition_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('base_historicaldefaulttransition_history_id_seq', 5, true);


--
-- Data for Name: base_historicalperson; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY base_historicalperson (id, name, surname, display_name, ssn, user_id, address_id, avatar, website, history_id, history_date, history_user_id, history_type) FROM stdin;
\.


--
-- Name: base_historicalperson_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('base_historicalperson_history_id_seq', 74, true);


--
-- Data for Name: base_historicalplace; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY base_historicalplace (id, name, description, address, zipcode, city, province, lon, lat, history_id, history_date, history_user_id, history_type) FROM stdin;
\.


--
-- Name: base_historicalplace_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('base_historicalplace_history_id_seq', 31, true);


--
-- Data for Name: base_person; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY base_person (id, name, surname, display_name, ssn, user_id, address_id, avatar, website) FROM stdin;
1	Referente informatico	Del test-des	Referente informatico del Test-Des	\N	1	\N		
2	Gasista_01	Delgas_01	Gasista_01 DelGas_01	\N	2	1		
3	Gasista_02	Delgas_01	Gasista_02 DelGas_01	\N	3	1		
4	Gasista_02	Delgas_02	Gasista_02 DelGas_02	\N	4	2		
7	Agente	02	Agente 02	\N	\N	2		
5	Gasista_01	Delgas_02	Gasista_01 DelGas_02	\N	5	2		
11	Nondes	Account	NonDES Account	\N	\N	\N		
12	Nondes	Account	NonDES Account	\N	\N	\N		
25	Riprovo	Ioriprovo	Riprovo Ioriprovo	\N	20	13		
26	Il finto	Finto	IL Finto finto	\N	21	14		
30	Agente	Orly1	Agente_ Orly1	\N	23	16		
6	Agente01	01	Agente01	\N	\N	1		
39	Gasper	01	Gasper 01	\N	32	26		
40	Gasper	02	Gasper 02	\N	33	27		
42	Nondes	Account	NonDES Account	\N	\N	\N		
43	Nondes	Account	NonDES Account	\N	\N	\N		
44	Utente	Generico	utente generico	\N	34	28		
46	Forni	Tore	forni tore	\N	36	29		
47	Referente	Economico	Referente Economico	\N	37	30		
23	Kobe	Bryan	Kobe Kobino	\N	18	11		
27	Luca	Elfero	Luca Ferroni	\N	22	13		
21	Orlando	Bloom	Orlando Marchetti	\N	16	9		
\.


--
-- Data for Name: base_person_contact_set; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY base_person_contact_set (id, person_id, contact_id) FROM stdin;
1	2	2
2	2	3
3	3	3
4	3	4
5	4	3
6	4	6
9	6	3
10	7	3
14	5	3
16	5	7
42	23	38
46	25	43
48	26	44
50	27	46
74	39	68
75	39	62
76	40	69
77	40	70
83	44	72
84	44	73
88	46	38
92	47	38
\.


--
-- Name: base_person_contact_set_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('base_person_contact_set_id_seq', 92, true);


--
-- Name: base_person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('base_person_id_seq', 47, true);


--
-- Data for Name: base_place; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY base_place (id, name, description, address, zipcode, city, province, lon, lat) FROM stdin;
1					Luogo01	MC	\N	\N
2					Luogo02	AN	\N	\N
3					Montecassiano		\N	\N
4					Montecassiano	MC	\N	\N
5					Montecassiano	MC	\N	\N
6	Ex mattatoio		Via della pace 223	62100	Macerata	MC	\N	\N
7					Macerata		\N	\N
9					Recanati		\N	\N
11					A		\N	\N
12					Marina di montemarciano		\N	\N
13					Fabriano		\N	\N
14					Finto		\N	\N
15					Recanati	MC	\N	\N
16	Produttore 1 principale				Recanati	MC	\N	\N
22					Fossombrone	PS	\N	\N
23					S.ippolito		\N	\N
24					Ascoli piceno	AP	\N	\N
25					Ascoli piceno		\N	\N
26					Gasper_01		\N	\N
27					Gasper_02		\N	\N
28					Luogo		\N	\N
29					Bruxelles		\N	\N
30					Amsterdam		\N	\N
\.


--
-- Name: base_place_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('base_place_id_seq', 30, true);


--
-- Data for Name: blockconfiguration; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY blockconfiguration (id, user_id, blocktype, resource_type, resource_id, page, "position", confdata) FROM stdin;
\.


--
-- Name: blockconfiguration_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('blockconfiguration_id_seq', 1, false);


--
-- Data for Name: captcha_captchastore; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY captcha_captchastore (id, challenge, response, hashkey, expiration) FROM stdin;
\.


--
-- Name: captcha_captchastore_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('captcha_captchastore_id_seq', 120, true);


--
-- Data for Name: des_des; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY des_des (site_ptr_id, cfg_time, logo) FROM stdin;
1	1425265683	
\.


--
-- Data for Name: des_des_info_people_set; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY des_des_info_people_set (id, des_id, person_id) FROM stdin;
\.


--
-- Name: des_des_info_people_set_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('des_des_info_people_set_id_seq', 1, false);


--
-- Data for Name: des_siteattr; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY des_siteattr (id, name, value, atype, descr) FROM stdin;
3	name	Test Des	varchar	Site name
1	descr	Gestionale degli ordini per i DES (Test-Des)	varchar	Site description
2	site_config_timestamp	1425265683	timestamp	Last site modification timestamp
\.


--
-- Name: des_siteattr_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('des_siteattr_id_seq', 3, true);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY django_admin_log (id, action_time, user_id, content_type_id, object_id, object_repr, action_flag, change_message) FROM stdin;
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 192, true);


--
-- Data for Name: django_comment_flags; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY django_comment_flags (id, user_id, comment_id, flag, flag_date) FROM stdin;
\.


--
-- Name: django_comment_flags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('django_comment_flags_id_seq', 1, false);


--
-- Data for Name: django_comments; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY django_comments (id, content_type_id, object_pk, site_id, user_id, user_name, user_email, user_url, comment, submit_date, ip_address, is_public, is_removed) FROM stdin;
5	78	4	1	2	01gas1	gasista01@gas01.test		èerche nn proviamo	2014-03-19 01:45:58.893795+01	\N	t	f
6	90	55	1	2	01gas1	gasista01@gas01.test		Ciao, ciao!	2014-05-07 22:46:31.116136+02	\N	t	f
\.


--
-- Name: django_comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('django_comments_id_seq', 6, true);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY django_content_type (id, name, app_label, model) FROM stdin;
1	permission	permissions	permission
2	object permission	permissions	objectpermission
3	object permission inheritance block	permissions	objectpermissioninheritanceblock
4	role	permissions	role
5	principal role relation	permissions	principalrolerelation
6	workflow	workflows	workflow
7	state	workflows	state
8	transition	workflows	transition
9	state object relation	workflows	stateobjectrelation
10	workflow object relation	workflows	workflowobjectrelation
11	workflow model relation	workflows	workflowmodelrelation
12	workflow permission relation	workflows	workflowpermissionrelation
13	state inheritance block	workflows	stateinheritanceblock
14	state permission relation	workflows	statepermissionrelation
15	Parameter	flexi_auth	param
16	Parametric Role	flexi_auth	paramrole
17	principal param role relation	flexi_auth	principalparamrolerelation
18	subject	simple_accounting	subject
19	account type	simple_accounting	accounttype
20	account system	simple_accounting	accountsystem
21	account	simple_accounting	account
22	cash flow	simple_accounting	cashflow
23	split	simple_accounting	split
24	transaction	simple_accounting	transaction
25	transaction reference	simple_accounting	transactionreference
26	ledger entry	simple_accounting	ledgerentry
27	invoice	simple_accounting	invoice
28	historical person	base	historicalperson
29	person	base	person
30	historical contact	base	historicalcontact
31	contact	base	contact
32	historical place	base	historicalplace
33	place	base	place
34	historical default transition	base	historicaldefaulttransition
35	default transition	base	defaulttransition
36	historical supplier	supplier	historicalsupplier
37	supplier	supplier	supplier
38	supplier config	supplier	supplierconfig
39	historical supplier agent	supplier	historicalsupplieragent
40	supplier agent	supplier	supplieragent
41	historical certification	supplier	historicalcertification
42	certification	supplier	certification
43	historical product category	supplier	historicalproductcategory
44	Product category	supplier	productcategory
45	historical product mu	supplier	historicalproductmu
46	measure unit	supplier	productmu
47	historical product pu	supplier	historicalproductpu
48	product unit	supplier	productpu
49	units conversion	supplier	unitsconversion
50	historical product	supplier	historicalproduct
51	product	supplier	product
52	historical supplier stock	supplier	historicalsupplierstock
53	supplier stock	supplier	supplierstock
54	supplier product category	supplier	supplierproductcategory
55	Block configuration data	rest	blockconfiguration
56	page	rest	page
57	home page	rest	homepage
58	permission	auth	permission
59	group	auth	group
60	user	auth	user
61	message	auth	message
62	content type	contenttypes	contenttype
63	session	sessions	session
64	site	sites	site
65	site	des	des
66	environment variable	des	siteattr
67	log entry	admin	logentry
68	comment	comments	comment
69	comment flag	comments	commentflag
70	notice type	notification	noticetype
71	notice setting	notification	noticesetting
72	notice	notification	notice
73	notice queue batch	notification	noticequeuebatch
74	observed item	notification	observeditem
75	registration profile	registration	registrationprofile
76	migration history	south	migrationhistory
77	historical gas	gas	historicalgas
78	gas	gas	gas
79	historical gas config	gas	historicalgasconfig
80	GAS options	gas	gasconfig
81	historical gas activist	gas	historicalgasactivist
82	GAS activist	gas	gasactivist
83	historical gas member	gas	historicalgasmember
84	GAS member	gas	gasmember
85	historical gas supplier stock	gas	historicalgassupplierstock
86	GAS supplier stock	gas	gassupplierstock
87	historical gas supplier solidal pact	gas	historicalgassuppliersolidalpact
88	gas supplier solidal pact	gas	gassuppliersolidalpact
89	historical gas supplier order	gas	historicalgassupplierorder
90	order issued to supplier	gas	gassupplierorder
91	historical gas supplier order product	gas	historicalgassupplierorderproduct
92	gas supplier order product	gas	gassupplierorderproduct
93	historical gas member order	gas	historicalgasmemberorder
94	GAS member order	gas	gasmemberorder
95	historical delivery	gas	historicaldelivery
96	delivery	gas	delivery
97	historical withdrawal	gas	historicalwithdrawal
98	wihtdrawal	gas	withdrawal
99	user profile	users	userprofile
100	captcha store	captcha	captchastore
101	person-contact relationship	base	person_contact_set
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('django_content_type_id_seq', 101, true);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
cf8d3caeccce1477393004d85f2fe056	OTVhN2ZlZTY0NmI5OTZmMzkyMGZjZjA1MWJmMTMwM2I2MjM1ZmMwYjqAAn1xAShVCnRlc3Rjb29r\naWVxAlUGd29ya2VkcQNVDGFwcF9zZXR0aW5nc3EEfXEFKFUFREVCVUdxBohVBVRIRU1FcQdVBW1p\nbGt5cQhVB1ZFUlNJT05xCVUEMC4xMXEKdXUu\n	2015-03-17 02:20:26.065857+01
3c0f771f80d0d4ee2e0a1e5d02db3f57	NjUzYjU3YmYzMzlmNmRmNzIzMGE4YWVlYTFjNTRhNWM4YmFjZTk2YjqAAn1xAVUMYXBwX3NldHRp\nbmdzcQJ9cQMoVQVERUJVR3EEiFUFVEhFTUVxBVUFbWlsa3lxBlUHVkVSU0lPTnEHVQQwLjExcQh1\ncy4=\n	2015-03-17 02:20:26.183167+01
f665e979a6a695e479b79d87c7d5f2c8	OTVhN2ZlZTY0NmI5OTZmMzkyMGZjZjA1MWJmMTMwM2I2MjM1ZmMwYjqAAn1xAShVCnRlc3Rjb29r\naWVxAlUGd29ya2VkcQNVDGFwcF9zZXR0aW5nc3EEfXEFKFUFREVCVUdxBohVBVRIRU1FcQdVBW1p\nbGt5cQhVB1ZFUlNJT05xCVUEMC4xMXEKdXUu\n	2015-03-17 02:30:26.925148+01
8d1d06019e857d0630760526c73d300f	NjUzYjU3YmYzMzlmNmRmNzIzMGE4YWVlYTFjNTRhNWM4YmFjZTk2YjqAAn1xAVUMYXBwX3NldHRp\nbmdzcQJ9cQMoVQVERUJVR3EEiFUFVEhFTUVxBVUFbWlsa3lxBlUHVkVSU0lPTnEHVQQwLjExcQh1\ncy4=\n	2015-03-17 02:30:27.059978+01
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY django_site (id, domain, name) FROM stdin;
1	beta.gasistafelice.befair.it	Test Des
\.


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('django_site_id_seq', 1, true);


--
-- Data for Name: flexi_auth_param; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY flexi_auth_param (id, name, content_type_id, object_id) FROM stdin;
1	des	65	1
2	gas	78	1
3	gas	78	2
4	supplier	37	1
5	supplier	37	2
6	pact	88	1
7	pact	88	2
8	pact	88	3
9	pact	88	4
10	gas	78	3
11	gas	78	4
12	pact	88	5
13	pact	88	6
14	supplier	37	3
15	pact	88	7
16	pact	88	8
17	supplier	37	4
18	pact	88	9
19	pact	88	10
20	supplier	37	5
21	supplier	37	6
22	gas	78	5
23	pact	88	11
24	pact	88	12
25	gas	78	6
26	pact	88	13
27	pact	88	14
28	pact	88	15
29	pact	88	16
30	pact	88	17
31	pact	88	18
\.


--
-- Name: flexi_auth_param_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('flexi_auth_param_id_seq', 31, true);


--
-- Data for Name: flexi_auth_paramrole; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY flexi_auth_paramrole (id, role_id) FROM stdin;
1	11
2	3
3	10
4	9
5	3
6	10
7	9
8	2
9	2
10	5
11	5
12	5
13	5
14	3
15	10
16	9
17	3
18	10
19	9
20	5
21	5
22	2
23	5
24	5
25	2
26	5
27	5
28	2
29	2
30	3
31	10
32	9
33	5
34	5
35	3
36	10
37	9
38	5
39	5
40	5
41	5
42	5
43	5
\.


--
-- Name: flexi_auth_paramrole_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('flexi_auth_paramrole_id_seq', 43, true);


--
-- Data for Name: flexi_auth_paramrole_param_set; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY flexi_auth_paramrole_param_set (id, paramrole_id, param_id) FROM stdin;
1	1	1
2	2	2
3	3	2
4	4	2
5	5	3
6	6	3
7	7	3
8	8	4
9	9	5
10	10	6
11	11	7
12	12	8
13	13	9
14	14	10
15	15	10
16	16	10
17	17	11
18	18	11
19	19	11
20	20	12
21	21	13
22	22	14
23	23	15
24	24	16
25	25	17
26	26	18
27	27	19
28	28	20
29	29	21
30	30	22
31	31	22
32	32	22
33	33	23
34	34	24
35	35	25
36	36	25
37	37	25
38	38	26
39	39	27
40	40	28
41	41	29
42	42	30
43	43	31
\.


--
-- Name: flexi_auth_paramrole_param_set_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('flexi_auth_paramrole_param_set_id_seq', 43, true);


--
-- Data for Name: flexi_auth_principalparamrolerelation; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY flexi_auth_principalparamrolerelation (id, user_id, group_id, role_id) FROM stdin;
1	1	\N	1
2	2	\N	2
3	3	\N	2
4	4	\N	5
5	5	\N	5
7	5	\N	6
8	4	\N	7
10	5	\N	10
11	4	\N	11
22	2	\N	5
23	4	\N	2
40	16	\N	17
42	18	\N	2
45	20	\N	2
46	21	\N	2
48	22	\N	22
50	16	\N	25
51	16	\N	26
53	23	\N	25
73	32	\N	35
74	33	\N	35
76	2	\N	43
77	34	\N	2
79	36	\N	8
80	37	\N	2
6	2	\N	3
9	3	\N	4
12	2	\N	12
13	3	\N	13
43	18	\N	12
47	20	\N	23
69	2	\N	38
81	37	\N	4
\.


--
-- Name: flexi_auth_principalparamrolerelation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('flexi_auth_principalparamrolerelation_id_seq', 81, true);


--
-- Data for Name: gas_delivery; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_delivery (id, place_id, date) FROM stdin;
1	1	2014-02-02 17:09:00+01
2	2	2014-02-02 17:11:00+01
3	2	2014-02-02 17:18:00+01
4	2	2014-03-02 18:16:00+01
33	1	2014-03-09 23:27:00+01
34	1	2014-03-09 23:43:00+01
35	1	2014-03-09 23:45:00+01
36	1	2014-03-09 01:00:00+01
37	5	2014-03-09 17:30:00+01
38	6	2014-03-07 18:30:00+01
39	22	2014-03-30 20:34:00+02
40	22	2014-03-30 20:37:00+02
41	1	2014-03-30 18:43:00+02
42	24	2014-04-06 19:24:00+02
43	24	2014-04-06 19:46:00+02
44	6	2014-04-04 18:30:00+02
45	1	2014-05-25 20:50:00+02
46	1	2014-05-25 21:50:00+02
47	1	2014-06-29 17:36:00+02
48	1	2014-06-29 17:40:00+02
49	1	2015-02-22 13:37:00+01
\.


--
-- Name: gas_delivery_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_delivery_id_seq', 49, true);


--
-- Data for Name: gas_gas; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_gas (id, name, id_in_des, logo, headquarter_id, description, membership_fee, birthday, vat, fcc, orders_email_contact_id, website, association_act, intent_act, note, des_id) FROM stdin;
2	Gas02	GA2		2		15.0000	2014-01-19			\N	\N				1
3	MonteGassiano	MGO		5		15.0000	2014-02-14			\N	\N				1
1	Gas01	GA1		1		20.0000	2014-01-19			\N	\N				1
4	Gas Macerata	GMC		6		20.0000	2014-02-14			\N	\N				1
5	Gas_Fossombrone	GAF		22		0.0000	2014-03-10			\N	\N				1
6	Gaspergas	GSG		24		15.0000	2014-03-10			\N	\N				1
\.


--
-- Data for Name: gas_gas_contact_set; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_gas_contact_set (id, gas_id, contact_id) FROM stdin;
2	2	5
3	3	14
5	1	1
\.


--
-- Name: gas_gas_contact_set_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_gas_contact_set_id_seq', 15, true);


--
-- Name: gas_gas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_gas_id_seq', 6, true);


--
-- Data for Name: gas_gasactivist; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_gasactivist (id, gas_id, person_id, info_title, info_description) FROM stdin;
\.


--
-- Name: gas_gasactivist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_gasactivist_id_seq', 1, false);


--
-- Data for Name: gas_gasconfig; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_gasconfig (id, gas_id, default_workflow_gasmember_order_id, default_workflow_gassupplier_order_id, can_change_price, order_show_only_next_delivery, order_show_only_one_at_a_time, default_close_day, default_delivery_day, default_close_time, default_delivery_time, use_withdrawal_place, can_change_withdrawal_place_on_each_order, can_change_delivery_place_on_each_order, default_withdrawal_place_id, default_delivery_place_id, auto_populate_products, use_scheduler, gasmember_auto_confirm_order, is_suspended, suspend_datetime, suspend_reason, suspend_auto_resume, notice_days_before_order_close, use_order_planning, send_email_on_order_close, registration_token, privacy_phone, privacy_email, privacy_cash) FROM stdin;
2	2	3	1	f	f	t			\N	\N	f	f	f	\N	\N	t	f	t	f	\N		\N	1	t	t		gas,suppliers	gas,suppliers	gas,suppliers
5	5	3	1	f	f	t			\N	\N	f	f	f	\N	\N	t	f	t	f	\N		\N	1	f	f		gas,suppliers	gas,suppliers	gas,suppliers
6	6	3	1	f	f	t			\N	\N	f	f	f	\N	\N	t	f	t	f	\N		\N	1	f	f		gas,suppliers	gas,suppliers	gas,suppliers
3	3	3	1	f	f	t			\N	\N	f	f	f	\N	\N	t	f	t	f	\N		\N	1	f	f		gas,suppliers	gas,suppliers	gas,suppliers
4	4	3	1	f	f	t	THURSDAY	FRIDAY	10:00:00	18:30:00	f	f	f	\N	\N	t	f	t	f	\N		\N	2	t	t	TOKENMACERATA1	gas,suppliers	gas,suppliers	gas,suppliers
1	1	3	1	f	f	f			\N	\N	f	f	f	\N	\N	t	f	t	f	\N		\N	1	t	f		gas,suppliers	gas,suppliers	gas,suppliers
\.


--
-- Name: gas_gasconfig_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_gasconfig_id_seq', 6, true);


--
-- Data for Name: gas_gasconfig_intergas_connection_set; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_gasconfig_intergas_connection_set (id, gasconfig_id, gas_id) FROM stdin;
2	2	1
19	3	2
20	3	4
21	4	2
22	4	3
23	1	2
\.


--
-- Name: gas_gasconfig_intergas_connection_set_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_gasconfig_intergas_connection_set_id_seq', 23, true);


--
-- Data for Name: gas_gasmember; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_gasmember (id, person_id, gas_id, id_in_gas, membership_fee_payed, use_planned_list, is_suspended, suspend_datetime, suspend_reason, suspend_auto_resume) FROM stdin;
1	2	1	\N	\N	f	f	\N		\N
2	3	1	\N	\N	f	f	\N		\N
3	4	2	\N	\N	f	f	\N		\N
4	5	2	\N	\N	f	f	\N		\N
6	2	2	\N	\N	f	f	\N		\N
7	4	1	\N	\N	f	f	\N		\N
20	23	1	\N	\N	f	f	\N		\N
21	25	1	\N	\N	f	f	\N		\N
22	26	1	\N	\N	f	f	\N		\N
28	39	6	\N	\N	f	f	\N		\N
29	40	6	\N	\N	f	f	\N		\N
30	44	1	\N	\N	f	f	\N		\N
32	47	1	\N	\N	f	f	\N		\N
\.


--
-- Data for Name: gas_gasmember_available_for_roles; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_gasmember_available_for_roles (id, gasmember_id, role_id) FROM stdin;
\.


--
-- Name: gas_gasmember_available_for_roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_gasmember_available_for_roles_id_seq', 1, false);


--
-- Name: gas_gasmember_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_gasmember_id_seq', 32, true);


--
-- Data for Name: gas_gasmemberorder; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_gasmemberorder (id, purchaser_id, ordered_product_id, ordered_price, ordered_amount, withdrawn_amount, is_confirmed, note) FROM stdin;
4	2	1	20.0000	1.00	\N	t	[ord da admin] 
5	4	4	20.0000	1.00	\N	t	[ord da admin] 
6	4	5	25.0000	1.00	\N	t	[ord da admin] 
10	4	9	40.0000	1.00	\N	t	[ord da admin] 
11	4	10	50.0000	1.00	\N	t	[ord da admin] 
12	2	7	40.0000	1.00	\N	t	[ord da admin] 
13	2	8	50.0000	1.00	\N	t	[ord da admin] 
14	3	9	40.0000	1.00	\N	t	[ord da admin] 
15	3	10	50.0000	1.00	\N	t	[ord da admin] 
1	1	1	20.0000	2.00	\N	t	[ord da admin] 
2	1	2	25.0000	2.00	\N	t	[ord da admin] 
3	1	3	10.0000	1.00	\N	t	[ord da admin] 
114	20	206	10.0000	9.00	\N	t	[ord da admin] 
9	1	8	50.0000	1.00	\N	t	[ord da admin] 
18	7	7	40.0000	1.00	\N	t	[ord da admin] 
19	7	8	50.0000	1.00	\N	t	[ord da admin] 
20	3	4	20.0000	1.00	\N	t	[ord da admin] 
7	3	5	25.0000	2.00	\N	t	[ord da admin] 
21	6	4	20.0000	1.00	\N	t	
22	6	5	25.0000	1.00	\N	t	
23	6	6	10.0000	1.00	\N	t	
24	3	11	20.0000	1.00	\N	t	
25	3	12	25.0000	1.00	\N	t	
26	3	13	10.0000	1.00	\N	t	
27	4	11	20.0000	1.00	\N	t	[ord da admin] 
28	4	12	25.0000	1.00	\N	t	[ord da admin] 
97	1	205	50.0000	1.00	\N	t	
32	21	106	4.5000	3.00	\N	t	
33	21	108	3.2500	3.00	\N	t	
34	21	109	3.0000	2.00	\N	t	
35	21	111	4.5000	3.00	\N	t	
36	21	113	5.0000	3.00	\N	t	
37	21	116	2.5600	4.00	\N	t	
43	1	110	2.5000	3.00	\N	t	[ord da admin] 
44	1	107	4.0000	3.00	\N	t	[ord da admin] 
45	2	113	5.0000	4.00	\N	t	[ord da admin] 
46	2	114	5.5000	3.00	\N	t	[ord da admin] 
47	21	96	10.0000	1.00	\N	t	[ord da admin] 
48	21	94	20.0000	1.00	\N	t	[ord da admin] 
49	21	95	25.0000	1.00	\N	t	[ord da admin] 
50	21	103	3.5000	1.00	\N	t	[ord da admin] 
98	1	201	20.0000	1.00	\N	t	
95	1	202	25.0000	1.00	\N	t	
96	1	203	3.5000	5.00	\N	t	
84	6	196	20.0000	2.00	\N	t	
85	4	196	20.0000	1.00	\N	t	[ord da admin] 
86	3	196	20.0000	1.00	\N	t	[ord da admin] 
87	3	197	200.0000	1.00	\N	t	[ord da admin] 
104	20	200	10.0000	1.00	\N	t	[ord da admin] 
105	20	201	20.0000	1.00	\N	t	[ord da admin] 
106	20	202	25.0000	1.00	\N	t	[ord da admin] 
107	20	203	3.5000	1.00	\N	t	[ord da admin] 
108	20	204	40.0000	1.00	\N	t	[ord da admin] 
109	20	205	50.0000	1.00	\N	t	[ord da admin] 
112	30	203	3.5000	2.00	\N	t	[ord da 01gas1] 
111	30	204	40.0000	1.00	\N	t	[ord da 01gas1] 
115	20	211	20.0000	4.00	\N	t	[ord da admin] 
116	20	207	20.0000	4.00	\N	t	CIAOCIAO
113	20	210	10.0000	5.00	\N	t	[ord da admin] 
\.


--
-- Name: gas_gasmemberorder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_gasmemberorder_id_seq', 116, true);


--
-- Data for Name: gas_gassupplierorder; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_gassupplierorder (id, pact_id, datetime_start, datetime_end, order_minimum_amount, delivery_id, withdrawal_id, delivery_cost, referrer_person_id, delivery_referrer_person_id, withdrawal_referrer_person_id, group_id, invoice_amount, invoice_note, root_plan_id) FROM stdin;
1	3	2014-01-19 17:00:00+01	2014-01-26 17:09:00+01	\N	1	\N	\N	2	\N	\N	\N	120.0000	totale fattura del yy/xx/anno	\N
2	1	2014-01-19 17:10:00+01	2014-01-26 17:11:00+01	\N	2	\N	\N	5	\N	\N	\N	170.0000	totale fattura del yy/xx/anno	\N
3	4	2014-01-19 17:10:00+01	2014-01-26 17:18:00+01	\N	\N	\N	\N	3	3	3	1	320.0000	totale fattura del yy/xx/anno	\N
4	2	2014-01-19 17:10:00+01	2014-01-26 17:18:00+01	\N	3	\N	\N	5	\N	\N	1	180.0000	pagamento fattura	\N
5	1	2014-02-13 18:10:00+01	2014-02-14 18:26:00+01	\N	4	\N	\N	4	\N	\N	\N	98.0000	qualcosa di simile	\N
34	3	2014-02-19 23:20:00+01	2014-03-02 23:27:00+01	\N	33	\N	\N	2	\N	\N	\N	\N		\N
35	3	2014-02-19 23:40:00+01	2014-03-02 23:43:00+01	\N	34	\N	\N	2	\N	\N	\N	\N		\N
36	3	2014-02-19 23:40:00+01	2014-03-02 23:45:00+01	\N	35	\N	\N	23	\N	\N	\N	\N		\N
40	9	2014-02-25 17:20:00+01	2014-03-06 10:00:00+01	\N	38	\N	\N	21	\N	\N	2	440.0000	pagamento fattura	\N
43	3	2014-03-12 18:40:00+01	2014-03-23 18:43:00+01	\N	41	\N	\N	2	\N	\N	\N	\N		\N
44	4	2014-03-19 18:40:00+01	2014-03-27 18:43:00+01	\N	41	\N	\N	3	\N	\N	\N	\N		\N
45	7	2014-03-12 18:40:00+01	2014-03-23 18:43:00+01	\N	41	\N	\N	25	\N	\N	\N	\N		\N
37	7	2014-02-20 01:00:00+01	2014-03-02 01:00:00+01	\N	36	\N	\N	25	\N	\N	\N	124.4900		\N
53	18	2014-04-23 11:50:00+02	\N	\N	\N	\N	\N	2	2	2	4	\N		\N
54	9	2014-04-23 11:50:00+02	\N	\N	\N	\N	\N	21	\N	\N	4	\N		\N
56	4	2014-05-07 21:50:00+02	2014-05-18 21:50:00+02	\N	46	\N	\N	2	\N	\N	\N	\N		\N
55	3	2014-05-07 20:50:00+02	2014-05-18 20:50:00+02	\N	45	\N	\N	2	\N	\N	\N	165.0000		\N
57	3	2014-06-12 17:30:00+02	2014-06-22 17:36:00+02	\N	47	\N	\N	2	\N	\N	\N	\N		\N
58	3	2014-06-12 17:40:00+02	2014-06-22 17:40:00+02	\N	48	\N	\N	2	\N	\N	\N	\N		\N
59	3	2015-02-02 13:30:00+01	2015-02-15 13:37:00+01	\N	49	\N	\N	2	\N	\N	\N	\N		\N
\.


--
-- Name: gas_gassupplierorder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_gassupplierorder_id_seq', 59, true);


--
-- Data for Name: gas_gassupplierorderproduct; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_gassupplierorderproduct (id, order_id, gasstock_id, maximum_amount, initial_price, order_price, delivered_price, delivered_amount) FROM stdin;
2	1	4	\N	25.0000	25.0000	25.0000	\N
3	1	6	\N	10.0000	10.0000	10.0000	\N
5	2	3	\N	25.0000	25.0000	25.0000	\N
6	2	5	\N	10.0000	10.0000	10.0000	\N
7	3	8	\N	40.0000	40.0000	40.0000	\N
8	3	10	\N	50.0000	50.0000	50.0000	\N
9	4	7	\N	40.0000	40.0000	40.0000	\N
10	4	9	\N	50.0000	50.0000	50.0000	\N
1	1	2	\N	20.0000	20.1000	20.0000	\N
4	2	1	\N	20.0000	20.0000	20.0000	\N
11	5	1	\N	20.0000	20.0000	20.0000	\N
12	5	3	\N	25.0000	25.0000	25.0000	\N
13	5	5	\N	10.0000	10.0000	10.0000	\N
94	34	2	\N	20.0000	20.0000	20.0000	\N
95	34	4	\N	25.0000	25.0000	25.0000	\N
96	34	6	\N	10.0000	10.0000	10.0000	\N
97	35	2	\N	20.0000	20.0000	20.0000	\N
98	35	4	\N	25.0000	25.0000	25.0000	\N
99	35	6	\N	10.0000	10.0000	10.0000	\N
100	36	2	\N	20.0000	20.0000	20.0000	\N
101	36	4	\N	25.0000	25.0000	25.0000	\N
102	36	6	\N	10.0000	10.0000	10.0000	\N
103	34	17	\N	3.5000	3.5000	3.5000	\N
104	35	17	\N	3.5000	3.5000	3.5000	\N
105	36	17	\N	3.5000	3.5000	3.5000	\N
106	37	19	\N	4.5000	4.5000	4.5000	\N
107	37	20	\N	4.0000	4.0000	4.0000	\N
108	37	21	\N	3.2500	3.2500	3.2500	\N
109	37	22	\N	3.0000	3.0000	3.0000	\N
110	37	23	\N	2.5000	2.5000	2.5000	\N
112	37	25	\N	4.0000	4.0000	4.0000	\N
111	37	24	\N	2.0000	4.5000	2.0000	\N
113	37	26	\N	5.0000	5.0000	5.0000	\N
114	37	27	\N	5.5000	5.5000	5.5000	\N
115	37	28	\N	6.0000	6.0000	6.0000	\N
116	37	29	\N	2.4600	2.5600	2.4600	\N
126	40	41	\N	20.0000	20.0000	20.0000	\N
127	40	42	\N	200.0000	200.0000	200.0000	\N
140	43	6	\N	10.0000	10.0000	10.0000	\N
141	43	2	\N	20.0000	20.0000	20.0000	\N
142	43	4	\N	25.0000	25.0000	25.0000	\N
143	43	17	\N	3.5000	3.5000	3.5000	\N
144	45	19	\N	4.5000	4.5000	4.5000	\N
145	45	20	\N	4.0000	4.0000	4.0000	\N
146	45	21	\N	3.2500	3.2500	3.2500	\N
147	45	22	\N	3.0000	3.0000	3.0000	\N
148	45	23	\N	2.5000	2.5000	2.5000	\N
149	45	24	\N	4.5000	4.5000	4.5000	\N
150	45	25	\N	4.0000	4.0000	4.0000	\N
151	45	26	\N	5.0000	5.0000	5.0000	\N
152	45	27	\N	5.5000	5.5000	5.5000	\N
153	45	28	\N	6.0000	6.0000	6.0000	\N
154	45	29	\N	2.5600	2.5600	2.5600	\N
155	45	58	\N	2.0000	2.0000	2.0000	\N
162	44	8	\N	40.0000	40.0000	40.0000	\N
163	44	10	\N	50.0000	50.0000	50.0000	\N
196	53	77	\N	20.0000	20.0000	20.0000	\N
197	53	78	\N	200.0000	200.0000	200.0000	\N
198	54	41	\N	20.0000	20.0000	20.0000	\N
199	54	42	\N	200.0000	200.0000	200.0000	\N
200	55	6	\N	10.0000	10.0000	10.0000	\N
201	55	2	\N	20.0000	20.0000	20.0000	\N
202	55	4	\N	25.0000	25.0000	25.0000	\N
203	55	17	\N	3.5000	3.5000	3.5000	\N
204	56	8	\N	40.0000	40.0000	40.0000	\N
205	56	10	\N	50.0000	50.0000	50.0000	\N
206	57	6	\N	10.0000	10.0000	10.0000	\N
207	57	2	\N	20.0000	20.0000	20.0000	\N
208	57	4	\N	25.0000	25.0000	25.0000	\N
209	57	17	\N	3.5000	3.5000	3.5000	\N
210	58	6	\N	10.0000	10.0000	10.0000	\N
211	58	2	\N	20.0000	20.0000	20.0000	\N
212	58	4	\N	25.0000	25.0000	25.0000	\N
213	58	17	\N	3.5000	3.5000	3.5000	\N
214	59	6	\N	10.0000	10.0000	10.0000	\N
215	59	2	\N	20.0000	20.0000	20.0000	\N
216	59	4	\N	25.0000	25.0000	25.0000	\N
217	59	17	\N	3.5000	3.5000	3.5000	\N
\.


--
-- Name: gas_gassupplierorderproduct_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_gassupplierorderproduct_id_seq', 217, true);


--
-- Data for Name: gas_gassuppliersolidalpact; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_gassuppliersolidalpact (id, gas_id, supplier_id, date_signed, order_minimum_amount, order_delivery_cost, order_deliver_interval, order_price_percent_update, default_delivery_day, default_delivery_time, default_delivery_place_id, auto_populate_products, orders_can_be_grouped, document, is_suspended, suspend_datetime, suspend_reason, suspend_auto_resume, send_email_on_order_close) FROM stdin;
1	2	1	2014-01-19	\N	\N	\N	\N		\N	\N	t	f		f	\N		\N	f
2	2	2	2014-01-19	\N	\N	\N	\N		\N	\N	t	f		f	\N		\N	f
5	4	1	2014-02-15	\N	\N	\N	\N		\N	\N	t	f		f	\N		\N	t
6	4	2	2014-02-15	\N	\N	\N	\N		\N	\N	t	f		f	\N		\N	f
7	1	3	2014-02-20	\N	\N	\N	\N		\N	\N	t	f		f	\N		\N	f
8	3	3	2014-02-20	200.0000	\N	\N	\N		\N	\N	t	f		f	\N		\N	f
9	4	4	2014-02-25	\N	\N	\N	\N		\N	\N	t	f		f	\N		\N	t
10	3	4	2014-02-25	\N	\N	\N	\N		\N	\N	t	f		f	\N		\N	f
11	5	3	2014-03-10	2000.0000	0.0000	19:30:00	\N		\N	\N	t	f		f	\N		\N	f
12	5	5	2014-03-10	100.0000	0.0000	20:30:00	\N		\N	\N	t	f		f	\N		\N	f
13	1	5	2014-03-12	\N	\N	\N	\N		\N	\N	t	f		f	\N		\N	f
3	1	1	2014-01-19	\N	\N	\N	\N		\N	\N	t	f		f	\N		\N	t
4	1	2	2014-01-19	\N	\N	\N	\N		\N	\N	t	f		f	\N		\N	t
14	6	6	2014-03-18	\N	\N	\N	\N		\N	\N	t	f		f	\N		\N	f
15	6	4	2014-03-18	\N	\N	\N	\N		\N	\N	t	f		f	\N		\N	f
16	6	1	2014-03-18	\N	\N	\N	\N		\N	\N	t	f		f	\N		\N	f
17	4	3	2014-03-25	\N	\N	\N	\N		\N	\N	t	f		f	\N		\N	f
18	2	4	2014-04-23	\N	\N	\N	\N		\N	\N	t	f		f	\N		\N	f
\.


--
-- Name: gas_gassuppliersolidalpact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_gassuppliersolidalpact_id_seq', 18, true);


--
-- Data for Name: gas_gassupplierstock; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_gassupplierstock (id, pact_id, stock_id, enabled, minimum_amount, step) FROM stdin;
5	1	3	t	1.00	1.00
6	3	3	t	1.00	1.00
7	2	4	t	1.00	1.00
8	4	4	t	1.00	1.00
9	2	5	t	1.00	1.00
10	4	5	t	1.00	1.00
1	1	1	t	1.00	1.00
2	3	1	t	1.00	1.00
3	1	2	t	1.00	1.00
4	3	2	t	1.00	1.00
11	5	3	t	1.00	1.00
12	5	2	t	1.00	1.00
13	5	1	t	1.00	1.00
14	6	5	t	1.00	1.00
15	6	4	t	1.00	1.00
16	5	6	t	1.00	1.00
17	3	6	t	1.00	1.00
18	1	6	t	1.00	1.00
30	8	17	f	1.00	1.00
31	8	16	f	1.00	1.00
32	8	15	f	1.00	1.00
33	8	14	f	1.00	1.00
34	8	13	t	1.00	1.00
35	8	12	t	1.00	1.00
36	8	11	t	1.00	1.00
37	8	10	t	1.00	1.00
38	8	9	t	1.00	1.00
39	8	8	t	1.00	1.00
40	8	7	t	1.00	1.00
41	9	19	t	1.00	1.00
42	9	18	t	1.00	1.00
43	10	19	t	1.00	1.00
44	10	18	t	1.00	1.00
45	11	17	t	1.00	1.00
46	11	16	t	1.00	1.00
47	11	15	t	1.00	1.00
48	11	14	t	1.00	1.00
49	11	13	t	1.00	1.00
50	11	12	t	1.00	1.00
51	11	11	t	1.00	1.00
52	11	10	t	1.00	1.00
53	11	9	t	1.00	1.00
54	11	8	t	1.00	1.00
55	11	7	t	1.00	1.00
56	11	20	t	4.00	2.00
57	8	20	t	4.00	2.00
59	15	19	t	1.00	1.00
60	15	18	t	1.00	1.00
61	16	3	t	1.00	1.00
62	16	2	t	1.00	1.00
63	16	1	t	1.00	1.00
64	16	6	t	1.00	1.00
19	7	11	t	1.00	1.00
20	7	10	t	1.00	1.00
21	7	9	t	1.00	1.00
22	7	8	t	1.00	1.00
23	7	7	t	1.00	1.00
24	7	12	t	1.00	1.00
25	7	13	t	1.00	1.00
26	7	14	t	1.00	1.00
27	7	15	t	1.00	1.00
28	7	16	t	1.00	1.00
29	7	17	t	1.00	1.00
58	7	20	t	4.00	2.00
65	17	17	t	1.00	1.00
66	17	12	t	1.00	1.00
67	17	16	t	1.00	1.00
68	17	15	t	1.00	1.00
69	17	14	t	1.00	1.00
70	17	13	t	1.00	1.00
71	17	7	t	1.00	1.00
72	17	11	t	1.00	1.00
73	17	10	t	1.00	1.00
74	17	9	t	1.00	1.00
75	17	8	t	1.00	1.00
76	17	20	t	4.00	2.00
77	18	19	t	1.00	1.00
78	18	18	t	1.00	1.00
\.


--
-- Name: gas_gassupplierstock_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_gassupplierstock_id_seq', 78, true);


--
-- Data for Name: gas_historicaldelivery; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_historicaldelivery (id, place_id, date, history_id, history_date, history_user_id, history_type) FROM stdin;
\.


--
-- Name: gas_historicaldelivery_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_historicaldelivery_history_id_seq', 49, true);


--
-- Data for Name: gas_historicalgas; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_historicalgas (id, name, id_in_des, logo, headquarter_id, description, membership_fee, birthday, vat, fcc, orders_email_contact_id, website, association_act, intent_act, note, des_id, history_id, history_date, history_user_id, history_type) FROM stdin;
\.


--
-- Name: gas_historicalgas_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_historicalgas_history_id_seq', 11, true);


--
-- Data for Name: gas_historicalgasactivist; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_historicalgasactivist (id, gas_id, person_id, info_title, info_description, history_id, history_date, history_user_id, history_type) FROM stdin;
\.


--
-- Name: gas_historicalgasactivist_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_historicalgasactivist_history_id_seq', 1, false);


--
-- Data for Name: gas_historicalgasconfig; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_historicalgasconfig (id, gas_id, default_workflow_gasmember_order_id, default_workflow_gassupplier_order_id, can_change_price, order_show_only_next_delivery, order_show_only_one_at_a_time, default_close_day, default_delivery_day, default_close_time, default_delivery_time, use_withdrawal_place, can_change_withdrawal_place_on_each_order, can_change_delivery_place_on_each_order, default_withdrawal_place_id, default_delivery_place_id, auto_populate_products, use_scheduler, gasmember_auto_confirm_order, is_suspended, suspend_datetime, suspend_reason, suspend_auto_resume, notice_days_before_order_close, history_id, history_date, history_user_id, history_type, use_order_planning, send_email_on_order_close, registration_token, privacy_phone, privacy_email, privacy_cash) FROM stdin;
\.


--
-- Name: gas_historicalgasconfig_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_historicalgasconfig_history_id_seq', 21, true);


--
-- Data for Name: gas_historicalgasmember; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_historicalgasmember (id, person_id, gas_id, id_in_gas, membership_fee_payed, history_id, history_date, history_user_id, history_type, use_planned_list, is_suspended, suspend_datetime, suspend_reason, suspend_auto_resume) FROM stdin;
\.


--
-- Name: gas_historicalgasmember_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_historicalgasmember_history_id_seq', 55, true);


--
-- Data for Name: gas_historicalgasmemberorder; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_historicalgasmemberorder (id, purchaser_id, ordered_product_id, ordered_price, ordered_amount, withdrawn_amount, is_confirmed, note, history_id, history_date, history_user_id, history_type) FROM stdin;
\.


--
-- Name: gas_historicalgasmemberorder_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_historicalgasmemberorder_history_id_seq', 225, true);


--
-- Data for Name: gas_historicalgassupplierorder; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_historicalgassupplierorder (id, pact_id, datetime_start, datetime_end, order_minimum_amount, delivery_id, withdrawal_id, delivery_cost, referrer_person_id, delivery_referrer_person_id, withdrawal_referrer_person_id, group_id, invoice_amount, invoice_note, root_plan_id, history_id, history_date, history_user_id, history_type) FROM stdin;
\.


--
-- Name: gas_historicalgassupplierorder_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_historicalgassupplierorder_history_id_seq', 107, true);


--
-- Data for Name: gas_historicalgassupplierorderproduct; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_historicalgassupplierorderproduct (id, order_id, gasstock_id, maximum_amount, initial_price, order_price, delivered_price, delivered_amount, history_id, history_date, history_user_id, history_type) FROM stdin;
\.


--
-- Name: gas_historicalgassupplierorderproduct_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_historicalgassupplierorderproduct_history_id_seq', 290, true);


--
-- Data for Name: gas_historicalgassuppliersolidalpact; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_historicalgassuppliersolidalpact (id, gas_id, supplier_id, date_signed, order_minimum_amount, order_delivery_cost, order_deliver_interval, order_price_percent_update, default_delivery_day, default_delivery_time, default_delivery_place_id, auto_populate_products, orders_can_be_grouped, document, is_suspended, suspend_datetime, suspend_reason, suspend_auto_resume, history_id, history_date, history_user_id, history_type, send_email_on_order_close) FROM stdin;
\.


--
-- Name: gas_historicalgassuppliersolidalpact_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_historicalgassuppliersolidalpact_history_id_seq', 22, true);


--
-- Data for Name: gas_historicalgassupplierstock; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_historicalgassupplierstock (id, pact_id, stock_id, enabled, minimum_amount, step, history_id, history_date, history_user_id, history_type) FROM stdin;
\.


--
-- Name: gas_historicalgassupplierstock_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_historicalgassupplierstock_history_id_seq', 117, true);


--
-- Data for Name: gas_historicalwithdrawal; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_historicalwithdrawal (id, place_id, date, start_time, end_time, history_id, history_date, history_user_id, history_type) FROM stdin;
\.


--
-- Name: gas_historicalwithdrawal_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_historicalwithdrawal_history_id_seq', 1, false);


--
-- Data for Name: gas_withdrawal; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY gas_withdrawal (id, place_id, date, start_time, end_time) FROM stdin;
\.


--
-- Name: gas_withdrawal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('gas_withdrawal_id_seq', 1, false);


--
-- Data for Name: notification_notice; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY notification_notice (id, recipient_id, sender_id, message, notice_type_id, added, unseen, archived, on_site) FROM stdin;
\.


--
-- Name: notification_notice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('notification_notice_id_seq', 64, true);


--
-- Data for Name: notification_noticequeuebatch; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY notification_noticequeuebatch (id, pickled_data) FROM stdin;
\.


--
-- Name: notification_noticequeuebatch_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('notification_noticequeuebatch_id_seq', 1, false);


--
-- Data for Name: notification_noticesetting; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY notification_noticesetting (id, user_id, notice_type_id, medium, send) FROM stdin;
1	2	4	0	t
2	5	4	0	t
3	3	4	0	t
4	3	5	0	t
5	5	5	0	t
6	2	5	0	t
7	4	4	0	t
18	18	4	0	t
19	20	4	0	t
21	16	4	0	t
\.


--
-- Name: notification_noticesetting_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('notification_noticesetting_id_seq', 24, true);


--
-- Data for Name: notification_noticetype; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY notification_noticetype (id, label, display, description, "default") FROM stdin;
1	gasmember_notification	Notification Received	you have received a notification	2
2	gas_notification	Notification Received	this GAS has received a notification	2
3	gas_newsletter	Newsletter Received	this GAS has received the newsletter	2
4	order_state_update	Order state updated	an order has been updated	2
5	ordered_product_update	Ordered product update	an ordered product has changed	3
564	gasstock_update	Product update for GAS	a product has been updated for GAS	3
\.


--
-- Name: notification_noticetype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('notification_noticetype_id_seq', 1260, true);


--
-- Data for Name: notification_observeditem; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY notification_observeditem (id, user_id, content_type_id, object_id, notice_type_id, added, signal) FROM stdin;
\.


--
-- Name: notification_observeditem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('notification_observeditem_id_seq', 1, false);


--
-- Data for Name: permissions_objectpermission; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY permissions_objectpermission (id, role_id, permission_id, content_type_id, content_id) FROM stdin;
\.


--
-- Name: permissions_objectpermission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('permissions_objectpermission_id_seq', 1, false);


--
-- Data for Name: permissions_objectpermissioninheritanceblock; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY permissions_objectpermissioninheritanceblock (id, permission_id, content_type_id, content_id) FROM stdin;
\.


--
-- Name: permissions_objectpermissioninheritanceblock_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('permissions_objectpermissioninheritanceblock_id_seq', 1, false);


--
-- Data for Name: permissions_permission; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY permissions_permission (id, name, codename) FROM stdin;
\.


--
-- Data for Name: permissions_permission_content_types; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY permissions_permission_content_types (id, permission_id, contenttype_id) FROM stdin;
\.


--
-- Name: permissions_permission_content_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('permissions_permission_content_types_id_seq', 1, false);


--
-- Name: permissions_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('permissions_permission_id_seq', 1, false);


--
-- Data for Name: permissions_principalrolerelation; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY permissions_principalrolerelation (id, user_id, group_id, role_id, content_type_id, content_id) FROM stdin;
\.


--
-- Name: permissions_principalrolerelation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('permissions_principalrolerelation_id_seq', 1, false);


--
-- Data for Name: permissions_role; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY permissions_role (id, name) FROM stdin;
1	NOBODY
2	SUPPLIER_REFERRER
3	GAS_MEMBER
4	GAS_REFERRER
5	GAS_REFERRER_SUPPLIER
6	GAS_REFERRER_ORDER
7	GAS_REFERRER_WITHDRAWAL
8	GAS_REFERRER_DELIVERY
9	GAS_REFERRER_CASH
10	GAS_REFERRER_TECH
11	DES_ADMIN
\.


--
-- Name: permissions_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('permissions_role_id_seq', 11, true);


--
-- Data for Name: registration_registrationprofile; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY registration_registrationprofile (id, user_id, activation_key) FROM stdin;
1	2	ALREADY_ACTIVATED
2	3	ALREADY_ACTIVATED
3	4	ALREADY_ACTIVATED
4	5	ALREADY_ACTIVATED
15	16	ALREADY_ACTIVATED
17	18	ALREADY_ACTIVATED
20	21	ALREADY_ACTIVATED
19	20	ALREADY_ACTIVATED
21	22	26fe909fc4e327598e20909dfcd6a93bdad884e6
22	23	ALREADY_ACTIVATED
31	32	ALREADY_ACTIVATED
32	33	ALREADY_ACTIVATED
33	34	ALREADY_ACTIVATED
35	36	ALREADY_ACTIVATED
36	37	ALREADY_ACTIVATED
\.


--
-- Name: registration_registrationprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('registration_registrationprofile_id_seq', 36, true);


--
-- Data for Name: rest_homepage; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY rest_homepage (id, role_id, user_id, resource_ctype_id, resource_id) FROM stdin;
\.


--
-- Name: rest_homepage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('rest_homepage_id_seq', 1, false);


--
-- Data for Name: rest_page; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY rest_page (id, role_id, user_id, resource_ctype_id, resource_id, confdata) FROM stdin;
\.


--
-- Name: rest_page_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('rest_page_id_seq', 1, false);


--
-- Data for Name: simple_accounting_account; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY simple_accounting_account (id, system_id, parent_id, name, kind_id, is_placeholder) FROM stdin;
1	1	\N		1	t
2	1	1	incomes	2	f
3	1	1	expenses	3	f
4	1	1	wallet	4	f
5	1	3	other	3	f
6	1	2	other	2	f
7	2	\N		1	t
8	2	7	incomes	2	f
9	2	7	expenses	3	f
10	2	7	cash	4	f
11	2	7	members	4	t
12	2	9	suppliers	3	t
13	2	8	recharges	2	f
14	2	8	fees	2	f
15	2	8	OutOfDES	2	f
16	2	9	OutOfDES	3	f
17	2	9	member	3	f
18	2	9	gas	3	f
19	2	8	member	2	f
20	3	\N		1	t
21	3	20	incomes	2	f
22	3	20	expenses	3	f
23	3	20	wallet	4	f
24	3	22	other	3	f
25	3	21	other	2	f
26	3	22	gas	3	t
27	3	26	gas-1	3	t
28	3	27	recharges	3	f
29	3	27	fees	3	f
30	2	11	person-2	4	f
31	4	\N		1	t
32	4	31	incomes	2	f
33	4	31	expenses	3	f
34	4	31	wallet	4	f
35	4	33	other	3	f
36	4	32	other	2	f
37	4	33	gas	3	t
38	4	37	gas-1	3	t
39	4	38	recharges	3	f
40	4	38	fees	3	f
41	2	11	person-3	4	f
42	5	\N		1	t
43	5	42	incomes	2	f
44	5	42	expenses	3	f
45	5	42	cash	4	f
46	5	42	members	4	t
47	5	44	suppliers	3	t
48	5	43	recharges	2	f
49	5	43	fees	2	f
50	5	43	OutOfDES	2	f
51	5	44	OutOfDES	3	f
52	5	44	member	3	f
53	5	44	gas	3	f
54	5	43	member	2	f
55	6	\N		1	t
56	6	55	incomes	2	f
57	6	55	expenses	3	f
58	6	55	wallet	4	f
59	6	57	other	3	f
60	6	56	other	2	f
61	6	57	gas	3	t
62	6	61	gas-2	3	t
63	6	62	recharges	3	f
64	6	62	fees	3	f
65	5	46	person-4	4	f
66	7	\N		1	t
67	7	66	incomes	2	f
68	7	66	expenses	3	f
69	7	66	wallet	4	f
70	7	68	other	3	f
71	7	67	other	2	f
72	7	68	gas	3	t
73	7	72	gas-2	3	t
74	7	73	recharges	3	f
75	7	73	fees	3	f
76	5	46	person-5	4	f
77	8	\N		1	t
78	8	77	incomes	2	f
79	8	77	expenses	3	f
80	8	77	wallet	4	f
81	8	79	other	3	f
82	8	78	other	2	f
83	9	\N		1	t
84	9	83	incomes	2	f
85	9	83	expenses	3	f
86	9	83	wallet	4	f
87	9	84	gas	2	t
88	10	\N		1	t
89	10	88	incomes	2	f
90	10	88	expenses	3	f
91	10	88	wallet	4	f
92	10	90	other	3	f
93	10	89	other	2	f
94	11	\N		1	t
95	11	94	incomes	2	f
96	11	94	expenses	3	f
97	11	94	wallet	4	f
98	11	95	gas	2	t
99	5	47	supplier-1	3	f
100	9	87	gas-2	2	f
101	5	47	supplier-2	3	f
102	11	98	gas-2	2	f
103	2	12	supplier-1	3	f
104	9	87	gas-1	2	f
105	2	12	supplier-2	3	f
106	11	98	gas-1	2	f
313	29	\N		1	t
314	29	313	incomes	2	f
315	29	313	expenses	3	f
316	29	313	wallet	4	f
317	29	315	other	3	f
318	29	314	other	2	f
123	2	11	person-9	4	f
124	3	26	gas-2	3	t
125	3	124	recharges	3	f
126	3	124	fees	3	f
127	5	46	person-2	4	f
128	6	61	gas-1	3	t
129	6	128	recharges	3	f
130	6	128	fees	3	f
131	2	11	person-4	4	f
132	11	96	gas	3	f
133	11	132	gas-1	3	f
134	2	8	suppliers	2	f
135	2	134	supplier-2	2	f
136	9	85	gas	3	f
137	9	136	gas-1	3	f
138	2	134	supplier-1	2	f
139	11	132	gas-2	3	f
140	5	43	suppliers	2	f
141	5	140	supplier-2	2	f
142	9	136	gas-2	3	f
143	5	140	supplier-1	2	f
144	14	\N		1	t
145	14	144	incomes	2	f
146	14	144	expenses	3	f
147	14	144	cash	4	f
148	14	144	members	4	t
149	14	146	suppliers	3	t
150	14	145	recharges	2	f
151	14	145	fees	2	f
152	14	145	OutOfDES	2	f
153	14	146	OutOfDES	3	f
154	14	146	member	3	f
155	14	146	gas	3	f
156	14	145	member	2	f
160	14	148	person-9	4	f
171	14	148	person-10	4	f
172	16	\N		1	t
173	16	172	incomes	2	f
174	16	172	expenses	3	f
175	16	172	cash	4	f
176	16	172	members	4	t
177	16	174	suppliers	3	t
178	16	173	recharges	2	f
179	16	173	fees	2	f
180	16	173	OutOfDES	2	f
181	16	174	OutOfDES	3	f
182	16	174	member	3	f
183	16	174	gas	3	f
184	16	173	member	2	f
185	17	\N		1	t
186	17	185	incomes	2	f
187	17	185	expenses	3	f
188	17	185	wallet	4	f
189	17	187	other	3	f
190	17	186	other	2	f
191	17	186	OutOfDES	2	f
192	18	\N		1	t
193	18	192	incomes	2	f
194	18	192	expenses	3	f
195	18	192	wallet	4	f
196	18	194	other	3	f
197	18	193	other	2	f
198	18	194	OutOfDES	3	f
209	16	176	person-13	4	f
319	29	315	gas	3	t
320	29	319	gas-1	3	t
321	29	320	recharges	3	f
322	29	320	fees	3	f
323	2	11	person-23	4	f
346	33	\N		1	t
347	33	346	incomes	2	f
348	33	346	expenses	3	f
349	33	346	wallet	4	f
350	33	348	other	3	f
351	33	347	other	2	f
352	33	348	gas	3	t
353	33	352	gas-1	3	t
354	33	353	recharges	3	f
355	33	353	fees	3	f
356	2	11	person-26	4	f
359	34	\N		1	t
360	34	359	incomes	2	f
361	34	359	expenses	3	f
362	34	359	wallet	4	f
363	34	361	other	3	f
364	34	360	other	2	f
368	14	149	supplier-3	3	f
369	30	328	gas-3	2	f
387	16	177	supplier-4	3	f
388	37	386	gas-4	2	f
391	37	384	gas	3	f
392	37	391	gas-3	3	f
393	14	145	suppliers	2	f
394	14	393	supplier-4	2	f
401	37	391	gas-4	3	f
402	16	173	suppliers	2	f
403	16	402	supplier-4	2	f
410	40	\N		1	t
411	40	410	incomes	2	f
412	40	410	expenses	3	f
413	40	410	wallet	4	f
414	40	411	gas	2	t
276	16	177	supplier-1	3	f
277	9	87	gas-4	2	f
278	16	177	supplier-2	3	f
279	11	98	gas-4	2	f
467	46	448	person-36	4	f
479	46	449	supplier-3	3	f
480	30	328	gas-5	2	f
486	46	448	person-9	4	f
291	27	\N		1	t
292	27	291	incomes	2	f
293	27	291	expenses	3	f
294	27	291	wallet	4	f
295	27	293	other	3	f
296	27	292	other	2	f
297	27	293	gas	3	t
298	27	297	gas-4	3	t
299	27	298	recharges	3	f
300	27	298	fees	3	f
301	16	176	person-21	4	f
324	30	\N		1	t
325	30	324	incomes	2	f
326	30	324	expenses	3	f
327	30	324	wallet	4	f
328	30	325	gas	2	t
335	32	\N		1	t
336	32	335	incomes	2	f
337	32	335	expenses	3	f
338	32	335	wallet	4	f
339	32	337	other	3	f
340	32	336	other	2	f
341	32	337	gas	3	t
342	32	341	gas-1	3	t
343	32	342	recharges	3	f
344	32	342	fees	3	f
345	2	11	person-25	4	f
357	2	12	supplier-3	3	f
358	30	328	gas-1	2	f
365	30	326	gas	3	f
366	30	365	gas-1	3	f
367	2	134	supplier-3	2	f
382	37	\N		1	t
383	37	382	incomes	2	f
384	37	382	expenses	3	f
385	37	382	wallet	4	f
386	37	383	gas	2	t
389	14	149	supplier-4	3	f
390	37	386	gas-3	2	f
395	38	\N		1	t
396	38	395	incomes	2	f
397	38	395	expenses	3	f
398	38	395	wallet	4	f
399	38	397	other	3	f
400	38	396	other	2	f
415	41	\N		1	t
416	41	415	incomes	2	f
417	41	415	expenses	3	f
418	41	415	wallet	4	f
419	41	416	gas	2	t
444	46	\N		1	t
445	46	444	incomes	2	f
446	46	444	expenses	3	f
447	46	444	cash	4	f
448	46	444	members	4	t
449	46	446	suppliers	3	t
450	46	445	recharges	2	f
451	46	445	fees	2	f
452	46	445	OutOfDES	2	f
453	46	446	OutOfDES	3	f
454	46	446	member	3	f
455	46	446	gas	3	f
456	46	445	member	2	f
478	46	448	person-37	4	f
481	46	449	supplier-5	3	f
482	40	414	gas-5	2	f
487	49	\N		1	t
488	49	487	incomes	2	f
489	49	487	expenses	3	f
490	49	487	cash	4	f
491	49	487	members	4	t
492	49	489	suppliers	3	t
493	49	488	recharges	2	f
494	49	488	fees	2	f
495	49	488	OutOfDES	2	f
496	49	489	OutOfDES	3	f
497	49	489	member	3	f
498	49	489	gas	3	f
499	49	488	member	2	f
510	49	491	person-38	4	f
511	9	136	gas-4	3	f
512	16	402	supplier-1	2	f
513	11	132	gas-4	3	f
514	16	402	supplier-2	2	f
515	40	412	gas	3	f
516	40	515	gas-5	3	f
517	46	445	suppliers	2	f
518	46	517	supplier-5	2	f
519	30	365	gas-5	3	f
520	46	517	supplier-3	2	f
521	30	365	gas-3	3	f
522	14	393	supplier-3	2	f
523	2	12	supplier-5	3	f
524	40	414	gas-1	2	f
525	49	492	supplier-6	3	f
526	41	419	gas-6	2	f
527	49	492	supplier-4	3	f
528	37	386	gas-6	2	f
529	49	492	supplier-1	3	f
530	9	87	gas-6	2	f
531	51	\N		1	t
532	51	531	incomes	2	f
533	51	531	expenses	3	f
534	51	531	wallet	4	f
535	51	533	other	3	f
536	51	532	other	2	f
537	51	533	gas	3	t
538	51	537	gas-6	3	t
539	51	538	recharges	3	f
540	51	538	fees	3	f
541	49	491	person-39	4	f
542	52	\N		1	t
543	52	542	incomes	2	f
544	52	542	expenses	3	f
545	52	542	wallet	4	f
546	52	544	other	3	f
547	52	543	other	2	f
548	52	544	gas	3	t
549	52	548	gas-6	3	t
550	52	549	recharges	3	f
551	52	549	fees	3	f
552	49	491	person-40	4	f
559	9	136	gas-6	3	f
560	49	488	suppliers	2	f
561	49	560	supplier-1	2	f
562	16	177	supplier-3	3	f
563	30	328	gas-4	2	f
564	37	391	gas-6	3	f
565	49	560	supplier-4	2	f
566	54	\N		1	t
567	54	566	incomes	2	f
568	54	566	expenses	3	f
569	54	566	wallet	4	f
570	54	568	other	3	f
571	54	567	other	2	f
572	54	568	OutOfDES	3	f
573	55	\N		1	t
574	55	573	incomes	2	f
575	55	573	expenses	3	f
576	55	573	wallet	4	f
577	55	575	other	3	f
578	55	574	other	2	f
579	55	575	OutOfDES	3	f
580	5	47	supplier-4	3	f
581	37	386	gas-2	2	f
582	56	\N		1	t
583	56	582	incomes	2	f
584	56	582	expenses	3	f
585	56	582	wallet	4	f
586	56	584	other	3	f
587	56	583	other	2	f
588	56	584	gas	3	t
589	56	588	gas-1	3	t
590	56	589	recharges	3	f
591	56	589	fees	3	f
592	2	11	person-44	4	f
603	16	176	person-45	4	f
604	37	391	gas-2	3	f
605	5	140	supplier-4	2	f
606	58	\N		1	t
607	58	606	incomes	2	f
608	58	606	expenses	3	f
609	58	606	wallet	4	f
610	58	608	other	3	f
611	58	607	other	2	f
612	59	\N		1	t
613	59	612	incomes	2	f
614	59	612	expenses	3	f
615	59	612	wallet	4	f
616	59	614	other	3	f
617	59	613	other	2	f
618	59	614	gas	3	t
619	59	618	gas-1	3	t
620	59	619	recharges	3	f
621	59	619	fees	3	f
622	2	11	person-47	4	f
\.


--
-- Name: simple_accounting_account_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('simple_accounting_account_id_seq', 622, true);


--
-- Data for Name: simple_accounting_accountsystem; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY simple_accounting_accountsystem (id, owner_id) FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
11	11
14	14
16	16
17	17
18	18
27	27
29	29
30	30
32	32
33	33
34	34
37	37
38	38
40	40
41	41
46	46
49	49
51	51
52	52
54	54
55	55
56	56
58	58
59	59
\.


--
-- Name: simple_accounting_accountsystem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('simple_accounting_accountsystem_id_seq', 59, true);


--
-- Data for Name: simple_accounting_accounttype; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY simple_accounting_accounttype (id, name, base_type) FROM stdin;
1	ROOT	0
2	INCOME	1
3	EXPENSE	2
4	ASSET	3
5	LIABILITY	4
\.


--
-- Name: simple_accounting_accounttype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('simple_accounting_accounttype_id_seq', 5, true);


--
-- Data for Name: simple_accounting_cashflow; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY simple_accounting_cashflow (id, account_id, amount) FROM stdin;
1	23	100.0000
2	30	-100.0000
3	23	50.0000
4	30	-50.0000
5	30	100.0000
6	10	-100.0000
7	41	20.0000
8	10	-20.0000
9	65	70.0000
10	45	-70.0000
11	76	45.0000
12	45	-45.0000
13	127	55.0000
14	45	-55.0000
15	30	50.0000
16	10	-50.0000
17	41	90.0000
18	10	-90.0000
19	123	90.0000
20	10	-90.0000
21	131	90.0000
22	10	-90.0000
23	10	120.0000
24	86	-120.0000
25	45	180.0000
26	97	-180.0000
27	23	500.0000
28	127	-500.0000
29	69	500.0000
30	76	-500.0000
31	58	500.0000
32	65	-500.0000
34	123	-500.0000
35	23	500.0000
36	30	-500.0000
37	34	500.0000
38	41	-500.0000
39	65	90.0000
40	45	-90.0000
41	76	90.0000
42	45	-90.0000
43	45	170.0000
44	86	-170.0000
45	10	320.0000
46	97	-320.0000
47	58	90.0000
48	131	-90.0000
49	10	10.0000
50	188	-10.0000
51	195	22.0000
52	10	-22.0000
55	65	55.4000
56	45	-55.4000
53	76	44.0200
54	45	-44.0200
57	45	100.0000
58	86	-100.0000
59	23	200.0000
60	30	-200.0000
61	34	200.0000
62	41	-200.0000
63	58	200.0000
64	131	-200.0000
65	316	200.0000
66	323	-200.0000
67	338	200.0000
68	345	-200.0000
70	123	-200.0000
71	127	15.0000
72	45	-15.0000
73	65	15.0000
74	45	-15.0000
75	76	15.0000
76	45	-15.0000
77	30	0.0000
78	10	0.0000
79	41	0.0000
80	10	0.0000
81	131	0.0000
82	10	0.0000
83	323	0.0000
84	10	0.0000
85	345	0.0000
86	10	0.0000
87	123	0.0000
88	10	0.0000
89	30	20.0000
90	10	-20.0000
91	41	20.0000
92	10	-20.0000
93	131	20.0000
94	10	-20.0000
95	323	20.0000
96	10	-20.0000
97	345	20.0000
98	10	-20.0000
99	123	20.0000
100	10	-20.0000
101	301	220.0000
102	175	-220.0000
103	209	220.0000
104	175	-220.0000
105	160	220.0000
106	147	-220.0000
107	171	220.0000
108	147	-220.0000
109	147	440.0000
110	385	-440.0000
111	175	440.0000
112	385	-440.0000
114	510	-200.0000
115	10	24.0000
116	30	-24.0000
117	30	704.0000
118	10	-704.0000
121	41	36.5000
122	10	-36.5000
123	345	67.9900
124	10	-67.9900
119	30	20.0000
120	10	-20.0000
125	510	200.0000
126	490	-200.0000
127	541	120.0000
128	490	-120.0000
129	552	100.0000
130	490	-100.0000
148	490	-100.0000
145	541	110.0000
146	490	-110.0000
158	490	-20.0000
135	510	220.0000
136	490	-220.0000
131	541	110.0000
132	490	-110.0000
133	552	110.0000
134	490	-110.0000
137	510	200.0000
138	490	-200.0000
139	541	0.0000
140	490	0.0000
141	552	0.0000
142	490	0.0000
159	510	0.0000
160	490	0.0000
147	552	100.0000
161	541	0.0000
162	490	0.0000
163	552	10.0000
143	510	210.0000
144	490	-210.0000
149	510	10.0000
150	490	-10.0000
151	541	10.0000
152	490	-10.0000
153	552	20.0000
154	490	-20.0000
155	510	40.5000
156	490	-40.5000
157	541	20.0000
164	490	-10.0000
165	510	-110.0000
166	490	110.0000
167	541	-10.0000
168	490	10.0000
169	552	-10.0000
170	490	10.0000
171	569	100.0000
172	147	-100.0000
173	576	100.0000
174	490	-100.0000
175	171	36.0000
176	147	-36.0000
177	147	36.0000
178	327	-36.0000
179	160	100.0000
180	147	-100.0000
181	171	100.0000
182	147	-100.0000
183	160	20.0000
184	147	-20.0000
185	171	40.0000
186	147	-40.0000
187	160	220.0000
188	147	-220.0000
189	171	200.0000
190	147	-200.0000
191	147	456.0000
192	327	-456.0000
193	30	62.5000
194	10	-62.5000
195	323	58.5000
196	10	-58.5000
197	123	33.5000
198	10	-33.5000
199	592	7.0000
200	10	-7.0000
201	30	2.0000
202	10	-2.0000
203	323	2.0000
204	10	-2.0000
205	123	-1.0000
206	10	1.0000
207	592	2.0000
208	10	-2.0000
209	10	165.0000
210	86	-165.0000
\.


--
-- Name: simple_accounting_cashflow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('simple_accounting_cashflow_id_seq', 210, true);


--
-- Data for Name: simple_accounting_invoice; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY simple_accounting_invoice (id, issuer_id, recipient_id, net_amount, taxes, issue_date, due_date, status, document) FROM stdin;
\.


--
-- Name: simple_accounting_invoice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('simple_accounting_invoice_id_seq', 1, false);


--
-- Data for Name: simple_accounting_ledgerentry; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY simple_accounting_ledgerentry (id, account_id, transaction_id, entry_id, amount, balance_current) FROM stdin;
12	10	4	11	20.0000	120.0000
20	10	8	13	50.0000	170.0000
22	10	9	21	90.0000	260.0000
24	10	10	23	90.0000	350.0000
26	10	11	25	90.0000	440.0000
27	10	12	27	-120.0000	320.0000
67	10	23	28	-320.0000	0.0000
82	10	26	76	22.0000	12.0000
39	69	15	1	-500.0000	-500.0000
116	45	36	88	15.0000	14.4200
30	86	12	1	120.0000	120.0000
87	45	29	87	-100.0000	-0.5800
122	10	39	83	0.0000	12.0000
124	10	40	123	0.0000	12.0000
126	10	41	125	0.0000	12.0000
128	10	42	127	0.0000	12.0000
130	10	43	129	0.0000	12.0000
132	10	44	131	0.0000	12.0000
134	10	45	133	20.0000	32.0000
136	10	46	135	20.0000	52.0000
138	10	47	137	20.0000	72.0000
140	10	48	139	20.0000	92.0000
142	10	49	141	20.0000	112.0000
3	13	1	1	100.0000	100.0000
7	13	2	4	50.0000	150.0000
53	13	18	50	500.0000	1150.0000
57	13	19	54	500.0000	1650.0000
73	13	24	58	90.0000	1740.0000
93	13	30	74	200.0000	1940.0000
97	13	31	94	200.0000	2140.0000
101	13	32	98	200.0000	2340.0000
105	13	33	102	200.0000	2540.0000
109	13	34	106	200.0000	2740.0000
81	15	26	1	22.0000	22.0000
1	23	1	1	-100.0000	-100.0000
5	23	2	2	-50.0000	-150.0000
35	23	14	6	-500.0000	-650.0000
51	23	18	36	-500.0000	-1150.0000
91	23	30	52	-200.0000	-1350.0000
2	24	1	1	100.0000	100.0000
6	24	2	3	50.0000	150.0000
36	24	14	7	500.0000	650.0000
52	24	18	37	500.0000	1150.0000
92	28	30	1	200.0000	200.0000
4	30	1	1	100.0000	100.0000
8	30	2	5	50.0000	150.0000
9	30	3	9	-100.0000	50.0000
19	30	8	10	-50.0000	0.0000
94	30	30	55	200.0000	700.0000
121	30	39	95	0.0000	700.0000
133	30	45	122	-20.0000	680.0000
55	34	19	1	-500.0000	-500.0000
95	34	31	56	-200.0000	-700.0000
56	35	19	1	500.0000	500.0000
96	39	31	1	200.0000	200.0000
11	41	4	1	-20.0000	-20.0000
21	41	9	12	-90.0000	-110.0000
58	41	19	22	500.0000	390.0000
98	41	31	59	200.0000	590.0000
123	41	40	99	0.0000	590.0000
14	45	5	1	70.0000	70.0000
16	45	6	15	45.0000	115.0000
18	45	7	17	55.0000	170.0000
31	45	13	19	-180.0000	-10.0000
60	45	20	32	90.0000	80.0000
62	45	21	61	90.0000	170.0000
63	45	22	63	-170.0000	0.0000
84	45	27	64	44.0200	44.0200
86	45	28	85	55.4000	99.4200
118	45	37	117	15.0000	29.4200
120	45	38	119	15.0000	44.4200
37	48	14	1	500.0000	500.0000
41	48	15	38	500.0000	1000.0000
43	58	16	1	-500.0000	-500.0000
71	58	24	44	-90.0000	-590.0000
99	58	32	72	-200.0000	-790.0000
44	59	16	1	500.0000	500.0000
72	59	24	45	90.0000	590.0000
13	65	5	1	-70.0000	-70.0000
46	65	16	14	500.0000	430.0000
59	65	20	47	-90.0000	340.0000
85	65	28	60	-55.4000	284.6000
117	65	37	86	-15.0000	269.6000
40	70	15	1	500.0000	500.0000
15	76	6	1	-45.0000	-45.0000
42	76	15	16	500.0000	455.0000
83	76	27	62	-44.0200	320.9800
119	76	38	84	-15.0000	305.9800
66	86	22	31	170.0000	290.0000
90	86	29	67	100.0000	390.0000
34	97	13	1	180.0000	180.0000
70	97	23	35	320.0000	500.0000
64	99	22	1	170.0000	170.0000
88	99	29	65	100.0000	270.0000
65	100	22	1	170.0000	170.0000
89	100	29	66	100.0000	270.0000
32	101	13	1	180.0000	180.0000
33	102	13	1	180.0000	180.0000
28	103	12	1	120.0000	120.0000
68	105	23	1	320.0000	320.0000
69	106	23	1	320.0000	320.0000
103	316	33	1	-200.0000	-200.0000
23	123	10	1	-90.0000	-90.0000
131	123	44	115	0.0000	610.0000
143	123	50	132	-20.0000	590.0000
17	127	7	1	-55.0000	-55.0000
115	127	36	39	-15.0000	430.0000
100	129	32	1	200.0000	200.0000
25	131	11	1	-90.0000	-90.0000
74	131	24	26	90.0000	0.0000
102	131	32	75	200.0000	200.0000
125	131	41	103	0.0000	200.0000
137	131	47	126	-20.0000	180.0000
146	175	51	1	220.0000	220.0000
78	188	25	1	10.0000	10.0000
77	191	25	1	10.0000	10.0000
79	195	26	1	-22.0000	-22.0000
80	198	26	1	22.0000	22.0000
104	321	33	1	200.0000	200.0000
127	323	42	107	0.0000	200.0000
139	323	48	128	-20.0000	180.0000
145	301	51	1	-220.0000	-220.0000
107	338	34	1	-200.0000	-200.0000
108	343	34	1	200.0000	200.0000
110	345	34	1	200.0000	200.0000
129	345	43	111	0.0000	200.0000
141	345	49	130	-20.0000	180.0000
203	510	75	198	-10.0000	-20.0000
232	490	87	225	100.0000	500.5000
233	171	88	152	-36.0000	-256.0000
234	147	88	229	36.0000	136.0000
235	147	89	235	-36.0000	100.0000
236	368	89	1	36.0000	36.0000
237	369	89	1	36.0000	36.0000
238	327	89	1	36.0000	36.0000
239	160	90	150	-100.0000	-320.0000
240	147	90	236	100.0000	200.0000
241	171	91	234	-100.0000	-356.0000
242	147	91	241	100.0000	300.0000
243	160	92	240	-20.0000	-340.0000
244	147	92	243	20.0000	320.0000
245	171	93	242	-40.0000	-396.0000
246	147	93	245	40.0000	360.0000
247	160	94	244	-220.0000	-560.0000
248	147	94	247	220.0000	580.0000
249	171	95	246	-200.0000	-596.0000
250	147	95	249	200.0000	780.0000
251	147	96	251	-456.0000	324.0000
252	368	96	237	456.0000	492.0000
253	369	96	238	456.0000	492.0000
254	327	96	239	456.0000	492.0000
255	30	97	174	-62.5000	-82.5000
256	10	97	179	62.5000	998.9900
257	323	98	140	-58.5000	121.5000
258	10	98	257	58.5000	1057.4900
259	123	99	144	-33.5000	556.5000
260	10	99	259	33.5000	1090.9900
261	592	100	1	-7.0000	-7.0000
262	10	100	261	7.0000	1097.9900
263	30	101	256	-2.0000	-84.5000
264	10	101	263	2.0000	1099.9900
265	323	102	258	-2.0000	119.5000
266	10	102	265	2.0000	1101.9900
10	10	3	1	100.0000	100.0000
75	10	25	68	-10.0000	-10.0000
144	10	50	143	20.0000	132.0000
165	10	58	145	-24.0000	108.0000
172	10	59	166	704.0000	812.0000
174	10	60	173	20.0000	832.0000
176	10	61	175	36.5000	868.5000
178	10	62	177	67.9900	936.4900
167	13	58	114	24.0000	2964.0000
76	16	25	1	10.0000	10.0000
166	17	58	1	24.0000	24.0000
170	18	59	1	704.0000	704.0000
171	19	59	1	704.0000	704.0000
54	30	18	20	500.0000	500.0000
168	30	58	134	24.0000	704.0000
169	30	59	169	-704.0000	0.0000
173	30	60	170	-20.0000	-20.0000
135	41	46	124	-20.0000	570.0000
175	41	61	136	-36.5000	533.5000
45	48	16	42	500.0000	1500.0000
61	76	21	43	-90.0000	365.0000
29	104	12	1	120.0000	120.0000
38	127	14	18	500.0000	445.0000
150	147	53	1	220.0000	220.0000
152	147	54	151	220.0000	440.0000
153	147	55	153	-440.0000	0.0000
149	160	53	1	-220.0000	-220.0000
151	171	54	1	-220.0000	-220.0000
148	175	52	147	220.0000	440.0000
157	175	56	149	-440.0000	0.0000
147	209	52	1	-220.0000	-220.0000
267	123	103	260	1.0000	557.5000
268	10	103	267	-1.0000	1100.9900
269	592	104	262	-2.0000	-9.0000
270	10	104	269	2.0000	1102.9900
106	323	33	1	200.0000	200.0000
158	387	56	1	440.0000	440.0000
159	388	56	1	440.0000	440.0000
271	10	105	271	-165.0000	937.9900
272	103	105	29	165.0000	285.0000
177	345	62	142	-67.9900	112.0100
156	385	55	1	440.0000	440.0000
160	385	56	157	440.0000	880.0000
154	389	55	1	440.0000	440.0000
155	390	55	1	440.0000	440.0000
198	490	72	1	210.0000	210.0000
200	490	73	199	110.0000	320.0000
202	490	74	201	100.0000	420.0000
197	510	72	165	-210.0000	-10.0000
199	541	73	1	-110.0000	-110.0000
201	552	74	1	-100.0000	-100.0000
204	490	75	203	10.0000	430.0000
205	541	76	200	-10.0000	-120.0000
206	490	76	205	10.0000	440.0000
207	552	77	202	-20.0000	-120.0000
208	490	77	207	20.0000	460.0000
209	510	78	204	-40.5000	-60.5000
210	490	78	209	40.5000	500.5000
211	541	79	206	-20.0000	-140.0000
212	490	79	211	20.0000	520.5000
213	510	80	210	0.0000	-60.5000
214	490	80	213	0.0000	520.5000
215	541	81	212	0.0000	-140.0000
216	490	81	215	0.0000	520.5000
217	552	82	208	-10.0000	-130.0000
218	490	82	217	10.0000	530.5000
219	510	83	214	110.0000	49.5000
220	490	83	219	-110.0000	420.5000
221	541	84	216	10.0000	-130.0000
222	490	84	221	-10.0000	410.5000
223	552	85	218	10.0000	-120.0000
224	490	85	223	-10.0000	400.5000
225	569	86	1	-100.0000	-100.0000
226	572	86	1	100.0000	100.0000
227	152	86	1	100.0000	100.0000
228	147	86	154	100.0000	100.0000
229	576	87	1	-100.0000	-100.0000
230	579	87	1	100.0000	100.0000
231	495	87	1	100.0000	100.0000
273	104	105	30	165.0000	285.0000
274	86	105	91	165.0000	555.0000
\.


--
-- Name: simple_accounting_ledgerentry_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('simple_accounting_ledgerentry_id_seq', 274, true);


--
-- Data for Name: simple_accounting_split; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY simple_accounting_split (id, exit_point_id, entry_point_id, target_id, description) FROM stdin;
1	24	13	2	
2	24	13	4	
3	\N	\N	6	
4	\N	\N	8	
5	\N	\N	10	
6	\N	\N	12	
7	\N	\N	14	
8	\N	\N	16	
9	\N	\N	18	
10	\N	\N	20	
11	\N	\N	22	
12	103	104	24	
13	101	102	26	
14	24	48	28	
15	70	48	30	
16	59	48	32	
18	24	13	36	
19	35	13	38	
20	\N	\N	40	
21	\N	\N	42	
22	99	100	44	
23	105	106	46	
24	59	13	48	
25	16	191	50	
26	198	15	52	
27	\N	\N	54	
28	\N	\N	56	
29	99	100	58	
30	28	13	60	
31	39	13	62	
32	129	13	64	
33	321	13	66	
34	343	13	68	
36	\N	\N	72	
37	\N	\N	74	
38	\N	\N	76	
39	\N	\N	78	
40	\N	\N	80	
41	\N	\N	82	
42	\N	\N	84	
43	\N	\N	86	
44	\N	\N	88	
45	\N	\N	90	
46	\N	\N	92	
47	\N	\N	94	
48	\N	\N	96	
49	\N	\N	98	
50	\N	\N	100	
51	\N	\N	102	
52	\N	\N	104	
53	\N	\N	106	
54	\N	\N	108	
55	389	390	110	
56	387	388	112	
58	17	13	116	
59	18	19	118	
60	\N	\N	120	
61	\N	\N	122	
62	\N	\N	124	
63	\N	\N	126	
64	\N	\N	128	
65	\N	\N	130	
66	\N	\N	132	
67	\N	\N	134	
68	\N	\N	136	
69	\N	\N	138	
70	\N	\N	140	
71	\N	\N	142	
72	\N	\N	144	
73	\N	\N	146	
74	\N	\N	148	
75	\N	\N	150	
76	\N	\N	152	
77	\N	\N	154	
78	\N	\N	156	
79	\N	\N	158	
80	\N	\N	160	
81	\N	\N	162	
82	\N	\N	164	
83	\N	\N	166	
84	\N	\N	168	
85	\N	\N	170	
86	572	152	172	
87	579	495	174	
88	\N	\N	176	
89	368	369	178	
90	\N	\N	180	
91	\N	\N	182	
92	\N	\N	184	
93	\N	\N	186	
94	\N	\N	188	
95	\N	\N	190	
96	368	369	192	
97	\N	\N	194	
98	\N	\N	196	
99	\N	\N	198	
100	\N	\N	200	
101	\N	\N	202	
102	\N	\N	204	
103	\N	\N	206	
104	\N	\N	208	
105	103	104	210	
\.


--
-- Name: simple_accounting_split_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('simple_accounting_split_id_seq', 105, true);


--
-- Data for Name: simple_accounting_subject; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY simple_accounting_subject (id, content_type_id, object_id) FROM stdin;
1	29	1
2	78	1
3	29	2
4	29	3
5	78	2
6	29	4
7	29	5
8	29	6
9	37	1
10	29	7
11	37	2
14	78	3
16	78	4
17	29	11
18	29	12
27	29	21
29	29	23
30	37	3
32	29	25
33	29	26
34	29	27
37	37	4
38	29	30
40	37	5
41	37	6
46	78	5
49	78	6
51	29	39
52	29	40
54	29	42
55	29	43
56	29	44
58	29	46
59	29	47
\.


--
-- Name: simple_accounting_subject_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('simple_accounting_subject_id_seq', 59, true);


--
-- Data for Name: simple_accounting_transaction; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY simple_accounting_transaction (id, date, description, issuer_id, source_id, kind, is_confirmed) FROM stdin;
1	2014-02-02 20:07:11.21781+01	GA1 LIABILITY Bonifico	3	1	ADJUST	f
2	2014-02-03 21:26:50.113375+01	GA1 LIABILITY felice	3	3	ADJUST	f
3	2014-02-08 00:24:26.357937+01	Ord. 1 GA1 - Fornitore 01	2	5	GAS_WITHDRAWAL	f
4	2014-02-08 00:24:26.430048+01	Ord. 1 GA1 - Fornitore 01	2	7	GAS_WITHDRAWAL	f
5	2014-02-08 02:54:46.155645+01	Ord. 2 GA2 - Fornitore 01	5	9	GAS_WITHDRAWAL	f
6	2014-02-08 02:54:46.226909+01	Ord. 2 GA2 - Fornitore 01	5	11	GAS_WITHDRAWAL	f
7	2014-02-08 02:54:46.284367+01	Ord. 2 GA2 - Fornitore 01	5	13	GAS_WITHDRAWAL	f
8	2014-02-08 02:58:54.345213+01	Ord. 3 GA1 - Fornitore 02	2	15	GAS_WITHDRAWAL	f
9	2014-02-08 02:58:54.450005+01	Ord. 3 GA1 - Fornitore 02	2	17	GAS_WITHDRAWAL	f
10	2014-02-08 02:58:54.53125+01	Ord. 3 GA1 - Fornitore 02	2	19	GAS_WITHDRAWAL	f
11	2014-02-08 02:58:54.614625+01	Ord. 3 GA1 - Fornitore 02	2	21	GAS_WITHDRAWAL	f
12	2014-02-08 03:02:48.572479+01	Ord. 1 GA1 - Fornitore 01. Pagamento fattura	2	23	PAYMENT	f
13	2014-02-08 03:09:49.399216+01	Ord. 4 GA2 - Fornitore 02. Pagamento fattura	5	25	PAYMENT	f
14	2014-02-08 16:37:40.859115+01	GA2 LIABILITY Ricarica effettuata dal box "Saldo" della scheda "Conto" dell' utente	3	27	ADJUST	f
15	2014-02-08 16:40:57.049309+01	GA2 LIABILITY Ricarica effettuata dal box "Saldo" della scheda "Conto" dell' utente	7	29	ADJUST	f
16	2014-02-08 16:41:30.007417+01	GA2 LIABILITY Ricarica effettuata dal box "Saldo" della scheda "Conto" dell' utente	6	31	ADJUST	f
19	2014-02-08 16:55:26.532277+01	GA1 LIABILITY Ricarica effettuata dal box "Saldo" della scheda "Conto" dell' utente	4	37	ADJUST	f
18	2014-02-08 16:54:38+01	GA1 LIABILITY Ricarica effettuata dal box "Saldo" della scheda "Conto" dell' utente e cambiata nell' interfaccia admin	3	35	ADJUST	f
20	2014-02-11 15:03:52.944151+01	Ord. 4 GA2 - Fornitore 02	5	39	GAS_WITHDRAWAL	f
21	2014-02-11 15:03:53.05823+01	Ord. 4 GA2 - Fornitore 02	5	41	GAS_WITHDRAWAL	f
22	2014-02-11 15:05:02.592636+01	Ord. 2 GA2 - Fornitore 01. Pagamento fattura	5	43	PAYMENT	f
23	2014-02-11 15:05:52.32844+01	Ord. 3 GA1 - Fornitore 02. Pagamento fattura	2	45	PAYMENT	f
24	2014-02-11 16:04:02.878449+01	GA1 LIABILITY Ricarica effettuata dal box "Saldo" della scheda "Conto" dell' utente	6	47	ADJUST	f
25	2014-02-14 19:24:46.832685+01	GA1 EXPENSE test 10 da dom Spesa	2	49	GAS_EXTRA	f
26	2014-02-14 19:26:03.926194+01	GA1 INCOME 22 di entrata	2	51	GAS_EXTRA	f
28	2014-02-14 19:29:21.977482+01	Ord. 5 GA2 - Fornitore 01. [MOD] new amount=55.4.	5	55	GAS_WITHDRAWAL	f
27	2014-02-14 19:29:12.737704+01	Ord. 5 GA2 - Fornitore 01. [MOD] new amount=44.02.	5	53	GAS_WITHDRAWAL	f
29	2014-02-14 19:48:36.880777+01	Ord. 5 GA2 - Fornitore 01. abbiamo dato 100	5	57	PAYMENT	f
30	2014-02-21 17:34:58.503789+01	Gasista_01 Delgas_01	3	59	RECHARGE	f
31	2014-02-21 17:34:58.778116+01	Gasista_02 Delgas_01	4	61	RECHARGE	f
32	2014-02-21 17:34:58.920454+01	Gasista_02 Delgas_02	6	63	RECHARGE	f
33	2014-02-21 17:34:59.056394+01	Antonio Esposito	29	65	RECHARGE	f
34	2014-02-21 17:34:59.182493+01	Riprovo Ioriprovo	32	67	RECHARGE	f
36	2014-02-24 18:12:44.17925+01	Anno 2014 --> Gasista_01 Delgas_01	5	71	MEMBERSHIP_FEE	f
37	2014-02-24 18:12:44.254164+01	Anno 2014 --> Gasista_02 Delgas_02	5	73	MEMBERSHIP_FEE	f
38	2014-02-24 18:12:44.320439+01	Anno 2014 --> Gasista_01 Delgas_02	5	75	MEMBERSHIP_FEE	f
39	2014-02-24 18:14:53.107409+01	Anno 2014 --> Gasista_01 Delgas_01	2	77	MEMBERSHIP_FEE	f
40	2014-02-24 18:14:53.179684+01	Anno 2014 --> Gasista_02 Delgas_01	2	79	MEMBERSHIP_FEE	f
41	2014-02-24 18:14:53.239134+01	Anno 2014 --> Gasista_02 Delgas_02	2	81	MEMBERSHIP_FEE	f
42	2014-02-24 18:14:53.294308+01	Anno 2014 --> Antonio Esposito	2	83	MEMBERSHIP_FEE	f
43	2014-02-24 18:14:53.3493+01	Anno 2014 --> Riprovo Ioriprovo	2	85	MEMBERSHIP_FEE	f
44	2014-02-24 18:14:53.408341+01	Anno 2014 --> Barbara Vecchi	2	87	MEMBERSHIP_FEE	f
45	2014-02-24 18:21:39.697503+01	Anno 2014 --> Gasista_01 Delgas_01	2	89	MEMBERSHIP_FEE	f
46	2014-02-24 18:21:39.769954+01	Anno 2014 --> Gasista_02 Delgas_01	2	91	MEMBERSHIP_FEE	f
47	2014-02-24 18:21:39.824062+01	Anno 2014 --> Gasista_02 Delgas_02	2	93	MEMBERSHIP_FEE	f
48	2014-02-24 18:21:39.881626+01	Anno 2014 --> Antonio Esposito	2	95	MEMBERSHIP_FEE	f
49	2014-02-24 18:21:39.944979+01	Anno 2014 --> Riprovo Ioriprovo	2	97	MEMBERSHIP_FEE	f
50	2014-02-24 18:21:40.012547+01	Anno 2014 --> Barbara Vecchi	2	99	MEMBERSHIP_FEE	f
51	2014-02-25 17:28:57.247459+01	Ord. 40 GMC - Alchemia	16	101	GAS_WITHDRAWAL	f
52	2014-02-25 17:28:57.357557+01	Ord. 40 GMC - Alchemia	16	103	GAS_WITHDRAWAL	f
53	2014-02-25 17:37:37.368202+01	Ord. 39 MGO - Alchemia	14	105	GAS_WITHDRAWAL	f
54	2014-02-25 17:37:37.493225+01	Ord. 39 MGO - Alchemia	14	107	GAS_WITHDRAWAL	f
55	2014-02-27 17:22:31.246596+01	Ord. 39 MGO - Alchemia. Pagamento fattura	14	109	PAYMENT	f
56	2014-02-27 17:23:30.373072+01	Ord. 40 GMC - Alchemia. Pagamento fattura	16	111	PAYMENT	f
58	2014-03-19 01:22:56.26334+01	GA1 INCOME propva 1	3	115	GASMEMBER_GAS	f
59	2014-03-19 01:23:38.670177+01	GA1 EXPENSE prova 2	3	117	GASMEMBER_GAS	f
61	2014-03-23 20:58:41.783238+01	Ord. 37 GA1 - La Terra E il Cielo Demo	2	121	GAS_WITHDRAWAL	f
62	2014-03-23 20:58:41.842006+01	Ord. 37 GA1 - La Terra E il Cielo Demo	2	123	GAS_WITHDRAWAL	f
60	2014-03-23 20:58:41.717708+01	Ord. 37 GA1 - La Terra E il Cielo Demo. [MOD] new amount=20.00.	2	119	GAS_WITHDRAWAL	f
72	2014-03-31 15:11:18.410214+02	Ord. 46 GSG - Alchemia. [MOD] new amount=210.00.. [MOD] new amount=200.00.. [MOD] new amount=210.00.	49	143	GAS_WITHDRAWAL	f
74	2014-03-31 15:11:18.569043+02	Ord. 46 GSG - Alchemia. [MOD] new amount=100.00.	49	147	GAS_WITHDRAWAL	f
73	2014-03-31 15:11:18.490703+02	Ord. 46 GSG - Alchemia. [MOD] new amount=100.00.. [MOD] new amount=110.00.	49	145	GAS_WITHDRAWAL	f
78	2014-04-01 18:01:19.543707+02	Ord. 47 GSG - Fornitore 01 ()	49	155	GAS_WITHDRAWAL	f
79	2014-04-01 18:01:19.63137+02	Ord. 47 GSG - Fornitore 01 ()	49	157	GAS_WITHDRAWAL	f
75	2014-04-01 17:57:10.091764+02	Ord. 46 GSG - Alchemia ([MOD] old_amount=210.0000 -> new_amount=220.00)	49	149	GAS_WITHDRAWAL	f
76	2014-04-01 17:57:10.338975+02	Ord. 46 GSG - Alchemia ([MOD] old_amount=110.0000 -> new_amount=120.00)	49	151	GAS_WITHDRAWAL	f
77	2014-04-01 17:57:10.564536+02	Ord. 46 GSG - Alchemia ([MOD] old_amount=100.0000 -> new_amount=120.00)	49	153	GAS_WITHDRAWAL	f
80	2014-04-01 18:01:39.185888+02	Ord. 47 GSG - Fornitore 01 ([MOD] old_amount=40.5000 -> new_amount=40.50)	49	159	GAS_WITHDRAWAL	f
81	2014-04-01 18:01:39.249301+02	Ord. 47 GSG - Fornitore 01 ([MOD] old_amount=20.0000 -> new_amount=20.00)	49	161	GAS_WITHDRAWAL	f
82	2014-04-01 18:06:02.926484+02	Ord. 47 GSG - Fornitore 01 ()	49	163	GAS_WITHDRAWAL	f
83	2014-04-01 18:18:42.734939+02	Ord. 46 GSG - Alchemia ([MOD] old_amount=220.00 -> new_amount=110.00)	49	165	GAS_WITHDRAWAL	f
84	2014-04-01 18:18:42.981714+02	Ord. 46 GSG - Alchemia ([MOD] old_amount=120.00 -> new_amount=110.00)	49	167	GAS_WITHDRAWAL	f
85	2014-04-01 18:18:43.216012+02	Ord. 46 GSG - Alchemia ([MOD] old_amount=120.00 -> new_amount=110.00)	49	169	GAS_WITHDRAWAL	f
86	2014-04-05 18:54:49.686961+02	MGO INCOME prova	14	171	GAS_EXTRA	f
87	2014-04-05 21:07:39.550273+02	GSG INCOME entrata di prova	49	173	GAS_EXTRA	f
88	2014-04-15 11:42:42.854063+02	Ord. 38 MGO - La Terra E il Cielo Demo	14	175	GAS_WITHDRAWAL	f
89	2014-04-15 12:14:57.685682+02	Ord. [38, 48] MGO - La Terra E il Cielo Demo. pagamento fattura	14	177	PAYMENT	f
90	2014-04-15 12:17:23.273608+02	Ord. 48 MGO - La Terra E il Cielo Demo	14	179	GAS_WITHDRAWAL	f
91	2014-04-15 12:17:35.888011+02	Ord. 48 MGO - La Terra E il Cielo Demo	14	181	GAS_WITHDRAWAL	f
92	2014-04-15 12:32:17.643848+02	Ord. 50 MGO - Alchemia	14	183	GAS_WITHDRAWAL	f
93	2014-04-15 12:32:31.664965+02	Ord. 50 MGO - Alchemia	14	185	GAS_WITHDRAWAL	f
94	2014-04-15 12:33:59.159873+02	Ord. 51 MGO - La Terra E il Cielo Demo	14	187	GAS_WITHDRAWAL	f
95	2014-04-15 12:34:11.828646+02	Ord. 51 MGO - La Terra E il Cielo Demo	14	189	GAS_WITHDRAWAL	f
96	2014-04-15 12:35:28.828061+02	Ord. [38, 51] MGO - La Terra E il Cielo Demo. pagamento fattura	14	191	PAYMENT	f
97	2014-05-07 23:00:43.929939+02	Ord. 55 GA1 - Fornitore 01	2	193	GAS_WITHDRAWAL	f
98	2014-05-07 23:00:44.095459+02	Ord. 55 GA1 - Fornitore 01	2	195	GAS_WITHDRAWAL	f
99	2014-05-07 23:00:44.25149+02	Ord. 55 GA1 - Fornitore 01	2	197	GAS_WITHDRAWAL	f
100	2014-05-07 23:00:44.395966+02	Ord. 55 GA1 - Fornitore 01	2	199	GAS_WITHDRAWAL	f
101	2014-05-07 23:01:31.261381+02	Ord. 55 GA1 - Fornitore 01 ([MOD] old_amount=62.50 -> new_amount=64.50)	2	201	GAS_WITHDRAWAL	f
102	2014-05-07 23:01:31.550204+02	Ord. 55 GA1 - Fornitore 01 ([MOD] old_amount=58.50 -> new_amount=60.50)	2	203	GAS_WITHDRAWAL	f
103	2014-05-07 23:01:31.834366+02	Ord. 55 GA1 - Fornitore 01 ([MOD] old_amount=33.50 -> new_amount=32.50)	2	205	GAS_WITHDRAWAL	f
104	2014-05-07 23:01:32.124915+02	Ord. 55 GA1 - Fornitore 01 ([MOD] old_amount=7.00 -> new_amount=9.00)	2	207	GAS_WITHDRAWAL	f
105	2014-05-07 23:11:26.849619+02	Ord. 55 GA1 - Fornitore 01. Fattura n.0101010	2	209	PAYMENT	f
\.


--
-- Name: simple_accounting_transaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('simple_accounting_transaction_id_seq', 105, true);


--
-- Data for Name: simple_accounting_transaction_split_set; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY simple_accounting_transaction_split_set (id, transaction_id, split_id) FROM stdin;
1	1	1
2	2	2
3	3	3
4	4	4
5	5	5
6	6	6
7	7	7
8	8	8
9	9	9
10	10	10
11	11	11
12	12	12
13	13	13
14	14	14
15	15	15
16	16	16
19	19	19
21	18	18
22	20	20
23	21	21
24	22	22
25	23	23
26	24	24
27	25	25
28	26	26
29	27	27
30	28	28
31	29	29
32	30	30
33	31	31
34	32	32
35	33	33
36	34	34
38	36	36
39	37	37
40	38	38
41	39	39
42	40	40
43	41	41
44	42	42
45	43	43
46	44	44
47	45	45
48	46	46
49	47	47
50	48	48
51	49	49
52	50	50
53	51	51
54	52	52
55	53	53
56	54	54
57	55	55
58	56	56
60	58	58
61	59	59
62	60	60
63	61	61
64	62	62
74	72	72
75	73	73
76	74	74
77	75	75
78	76	76
79	77	77
80	78	78
81	79	79
82	80	80
83	81	81
84	82	82
85	83	83
86	84	84
87	85	85
88	86	86
89	87	87
90	88	88
91	89	89
92	90	90
93	91	91
94	92	92
95	93	93
96	94	94
97	95	95
98	96	96
99	97	97
100	98	98
101	99	99
102	100	100
103	101	101
104	102	102
105	103	103
106	104	104
107	105	105
\.


--
-- Name: simple_accounting_transaction_split_set_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('simple_accounting_transaction_split_set_id_seq', 107, true);


--
-- Data for Name: simple_accounting_transactionreference; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY simple_accounting_transactionreference (id, transaction_id, content_type_id, object_id) FROM stdin;
1	3	84	1
2	3	90	1
3	4	84	2
4	4	90	1
5	5	84	3
6	5	90	2
7	6	84	4
8	6	90	2
9	7	84	6
10	7	90	2
11	8	84	1
12	8	90	3
13	9	84	2
14	9	90	3
15	10	84	5
16	10	90	3
17	11	84	7
18	11	90	3
19	12	90	1
20	13	90	4
21	20	84	3
22	20	90	4
23	21	84	4
24	21	90	4
25	22	90	2
26	23	90	3
27	27	84	4
28	27	90	5
29	28	84	3
30	28	90	5
31	29	90	5
32	30	29	2
33	30	78	1
34	31	29	3
35	31	78	1
36	32	29	4
37	32	78	1
38	33	29	23
39	33	78	1
40	34	29	25
41	34	78	1
44	36	29	2
45	36	78	2
46	37	29	4
47	37	78	2
48	38	29	5
49	38	78	2
50	39	29	2
51	39	78	1
52	40	29	3
53	40	78	1
54	41	29	4
55	41	78	1
56	42	29	23
57	42	78	1
58	43	29	25
59	43	78	1
60	44	29	9
61	44	78	1
62	45	29	2
63	45	78	1
64	46	29	3
65	46	78	1
66	47	29	4
67	47	78	1
68	48	29	23
69	48	78	1
70	49	29	25
71	49	78	1
72	50	29	9
73	50	78	1
74	51	84	18
75	51	90	40
76	52	84	10
77	52	90	40
78	53	84	8
79	53	90	39
80	54	84	9
81	54	90	39
82	55	90	39
83	56	90	40
86	60	84	1
87	60	90	37
88	61	84	2
89	61	90	37
90	62	84	21
91	62	90	37
110	72	84	27
111	72	90	46
112	73	84	28
113	73	90	46
114	74	84	29
115	74	90	46
116	75	84	27
117	75	90	46
118	76	84	28
119	76	90	46
120	77	84	29
121	77	90	46
122	78	84	27
123	78	90	47
124	79	84	28
125	79	90	47
126	80	84	27
127	80	90	47
128	81	84	28
129	81	90	47
130	82	84	29
131	82	90	47
132	83	84	27
133	83	90	46
134	84	84	28
135	84	90	46
136	85	84	29
137	85	90	46
138	88	84	9
139	88	90	38
140	89	90	38
141	89	90	48
142	90	84	8
143	90	90	48
144	91	84	9
145	91	90	48
146	92	84	8
147	92	90	50
148	93	84	9
149	93	90	50
150	94	84	8
151	94	90	51
152	95	84	9
153	95	90	51
154	96	90	38
155	96	90	51
156	97	84	1
157	97	90	55
158	98	84	20
159	98	90	55
160	99	84	5
161	99	90	55
162	100	84	30
163	100	90	55
164	101	84	1
165	101	90	55
166	102	84	20
167	102	90	55
168	103	84	5
169	103	90	55
170	104	84	30
171	104	90	55
172	105	90	55
\.


--
-- Name: simple_accounting_transactionreference_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('simple_accounting_transactionreference_id_seq', 172, true);


--
-- Data for Name: south_migrationhistory; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY south_migrationhistory (id, app_name, migration, applied) FROM stdin;
1	gas	0001_initial	2014-01-18 01:20:03.464319+01
2	gas	0002_auto__add_field_historicalgasconfig_use_order_planning__add_field_hist	2014-01-18 01:20:04.255889+01
3	gas	0003_auto__del_field_historicalgasconfig_is_active__del_field_gasconfig_is_	2014-01-18 01:20:04.561149+01
4	users	0001_initial	2014-01-18 01:20:05.836112+01
5	users	0002_auto__chg_field_userprofile_default_role	2014-01-18 01:20:05.941668+01
6	captcha	0001_initial	2014-01-18 01:20:06.79243+01
\.


--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('south_migrationhistory_id_seq', 6, true);


--
-- Data for Name: supplier_certification; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_certification (id, name, symbol, description) FROM stdin;
1	Certificato::Auto Certificazione	AC	Certificato::Auto Certificazione
2	Certificato::Certificato da IMC	IMC	Certificato::Certificato da IMC
3	In conversione	INC	In conversione
4	Convenzionale	BAD	Convenzionale
5	Certificato	Cert	Certificato
6	Certificato::Certificato da Suolo e Salute	SES	Certificato::Certificato da Suolo e Salute
7	Certificato::Certificato da ICEA	ICEA	Certificato::Certificato da ICEA
8	Certificato::PGS	PGS	Certificato::PGS
9	Privato	PRIVA	Privato
\.


--
-- Name: supplier_certification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_certification_id_seq', 9, true);


--
-- Data for Name: supplier_historicalcertification; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_historicalcertification (id, name, symbol, description, history_id, history_date, history_user_id, history_type) FROM stdin;
\.


--
-- Name: supplier_historicalcertification_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_historicalcertification_history_id_seq', 7560, true);


--
-- Data for Name: supplier_historicalproduct; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_historicalproduct (id, code, producer_id, category_id, mu_id, pu_id, muppu, muppu_is_variable, vat_percent, name, description, deleted, history_id, history_date, history_user_id, history_type) FROM stdin;
\.


--
-- Name: supplier_historicalproduct_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_historicalproduct_history_id_seq', 35, true);


--
-- Data for Name: supplier_historicalproductcategory; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_historicalproductcategory (id, name, description, image, history_id, history_date, history_user_id, history_type) FROM stdin;
\.


--
-- Name: supplier_historicalproductcategory_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_historicalproductcategory_history_id_seq', 68040, true);


--
-- Data for Name: supplier_historicalproductmu; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_historicalproductmu (id, name, symbol, history_id, history_date, history_user_id, history_type) FROM stdin;
\.


--
-- Name: supplier_historicalproductmu_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_historicalproductmu_history_id_seq', 5880, true);


--
-- Data for Name: supplier_historicalproductpu; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_historicalproductpu (id, name, symbol, description, history_id, history_date, history_user_id, history_type) FROM stdin;
\.


--
-- Name: supplier_historicalproductpu_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_historicalproductpu_history_id_seq', 7561, true);


--
-- Data for Name: supplier_historicalsupplier; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_historicalsupplier (id, name, seat_id, vat_number, ssn, website, frontman_id, flavour, n_employers, logo, iban, description, history_id, history_date, history_user_id, history_type) FROM stdin;
\.


--
-- Name: supplier_historicalsupplier_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_historicalsupplier_history_id_seq', 22, true);


--
-- Data for Name: supplier_historicalsupplieragent; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_historicalsupplieragent (id, supplier_id, person_id, job_title, job_description, history_id, history_date, history_user_id, history_type) FROM stdin;
\.


--
-- Name: supplier_historicalsupplieragent_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_historicalsupplieragent_history_id_seq', 1, false);


--
-- Data for Name: supplier_historicalsupplierstock; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_historicalsupplierstock (id, supplier_id, product_id, supplier_category_id, image, price, code, amount_available, units_minimum_amount, units_per_box, detail_minimum_amount, detail_step, delivery_notes, deleted, history_id, history_date, history_user_id, history_type) FROM stdin;
\.


--
-- Name: supplier_historicalsupplierstock_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_historicalsupplierstock_history_id_seq', 35, true);


--
-- Data for Name: supplier_product; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_product (id, code, producer_id, category_id, mu_id, pu_id, muppu, muppu_is_variable, vat_percent, name, description, deleted) FROM stdin;
3	\N	1	4	\N	5	1.00	f	0.21	Scarpe bambino/a		f
4	\N	2	10	\N	5	1.00	f	0.21	Blue-jeans Uomo	I jeans sono un tessuto inventato in Italia indossato molto probabilmente dai marinai genovesi infatti la parola Jean significa "blu di Genova"	f
5	\N	2	9	\N	5	1.00	f	0.21	Blue-jeans Donna		f
1	\N	1	6	\N	17	1.00	f	0.22	Scarpe Uomo		f
2	\N	1	5	\N	17	1.00	f	0.21	Scarpe Donna		f
6	\N	1	39	5	5	500.00	f	0.22	ORECCHIETTE		f
7	\N	3	41	5	5	500.00	f	0.22	SPAGHETTI		f
10	\N	3	41	5	5	500.00	f	0.22	FUSILLI		f
9	\N	3	41	5	5	500.00	f	0.22	PENNE RIGATE		f
8	\N	3	41	5	5	500.00	f	0.22	LINGUINE		f
11	\N	3	41	5	5	500.00	f	0.22	FILINI		f
12	\N	3	40	5	5	500.00	f	0.22	SPAGHETTI TR. AL BR.		f
13	\N	3	40	5	5	500.00	f	0.22	LINGUINE TR. AL BR.		f
14	\N	3	40	5	5	500.00	f	0.22	PENNE RIGATE TR. AL BR.		f
15	\N	3	40	5	5	500.00	f	0.22	FUSILLI TR. AL BR.		f
16	\N	3	40	5	5	500.00	f	0.22	TRENNE TR. AL BR.		f
17	\N	3	39	5	15	500.00	f	0.04	SPAGHETTI DI FARRO INTEGRALE GR. 500		f
18	\N	4	16	5	5	0.10	f	0.21	Pietra Filosofale macinata		f
19	\N	4	16	1	1	10.00	f	0.21	Elisir di lunga vita		f
20	\N	3	42	6	15	1.00	f	0.22	penne		f
\.


--
-- Name: supplier_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_product_id_seq', 20, true);


--
-- Data for Name: supplier_productcategory; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_productcategory (id, name, description, image) FROM stdin;
11	Alimenti 	description for category and subcategory Alimenti 	
14	Alimenti::Bevande::Birra 	description for category and subcategory Alimenti::Bevande::Birra 	
15	Alimenti::Bevande::Caffè 	description for category and subcategory Alimenti::Bevande::Caffè 	
16	Alimenti::Bevande::Tisane e Infusi 	description for category and subcategory Alimenti::Bevande::Tisane e Infusi 	
17	Alimenti::Bevande::Liquori 	description for category and subcategory Alimenti::Bevande::Liquori 	
18	Alimenti::Bevande::Tè	description for category and subcategory Alimenti::Bevande::Tè	
19	Alimenti::Bevande::Vino Bianco	description for category and subcategory Alimenti::Bevande::Vino Bianco	
20	Alimenti::Bevande::Vino Rosso	description for category and subcategory Alimenti::Bevande::Vino Rosso	
21	Alimenti::Carne::Bianca 	description for category and subcategory Alimenti::Carne::Bianca 	
22	Alimenti::Carne::Rossa 	description for category and subcategory Alimenti::Carne::Rossa 	
23	Alimenti::Conserve 	description for category and subcategory Alimenti::Conserve 	
24	Alimenti::Conserve::Marmellate 	description for category and subcategory Alimenti::Conserve::Marmellate 	
25	Alimenti::Conserve::Sughi pronti 	description for category and subcategory Alimenti::Conserve::Sughi pronti 	
26	Alimenti::Formaggi e latticini 	description for category and subcategory Alimenti::Formaggi e latticini 	
27	Alimenti::Formaggi e latticini::Formaggi freschi 	description for category and subcategory Alimenti::Formaggi e latticini::Formaggi freschi 	
29	Alimenti::Frutta	description for category and subcategory Alimenti::Frutta	
1	Abbigliamento 	description for category and subcategory Abbigliamento 	
28	Alimenti::Formaggi e latticini::Formaggi stagionati 	description for category and subcategory Alimenti::Formaggi e latticini::Formaggi stagionati 	
30	Alimenti::Frutta::Agrumi 	description for category and subcategory Alimenti::Frutta::Agrumi 	
31	Alimenti::Frutta::Frutta fresca 	description for category and subcategory Alimenti::Frutta::Frutta fresca 	
32	Alimenti::Frutta::Frutta secca 	description for category and subcategory Alimenti::Frutta::Frutta secca 	
33	Alimenti::Latte	description for category and subcategory Alimenti::Latte	
34	Alimenti::Legumi secchi	description for category and subcategory Alimenti::Legumi secchi	
35	Alimenti::Miele 	description for category and subcategory Alimenti::Miele 	
36	Alimenti::Olio 	description for category and subcategory Alimenti::Olio 	
37	Alimenti::Olio::Olio d'oliva 	description for category and subcategory Alimenti::Olio::Olio d'oliva 	
38	Alimenti::Olio::Olio di semi 	description for category and subcategory Alimenti::Olio::Olio di semi 	
39	Alimenti::Pasta 	description for category and subcategory Alimenti::Pasta 	
40	Alimenti::Pasta::Pasta di semola di grano duro 	description for category and subcategory Alimenti::Pasta::Pasta di semola di grano duro 	
41	Alimenti::Pasta::Pasta integrale di grano duro 	description for category and subcategory Alimenti::Pasta::Pasta integrale di grano duro 	
42	Alimenti::Pasta::Pasta semi-integrale	description for category and subcategory Alimenti::Pasta::Pasta semi-integrale	
43	Alimenti::Pesce	description for category and subcategory Alimenti::Pesce	
44	Alimenti::Prodotti da forno 	description for category and subcategory Alimenti::Prodotti da forno 	
45	Alimenti::Prodotti da forno::Biscotti 	description for category and subcategory Alimenti::Prodotti da forno::Biscotti 	
46	Alimenti::Prodotti da forno::Dolci 	description for category and subcategory Alimenti::Prodotti da forno::Dolci 	
47	Alimenti::Prodotti da forno::Pane 	description for category and subcategory Alimenti::Prodotti da forno::Pane 	
48	Alimenti::Riso 	description for category and subcategory Alimenti::Riso 	
49	Alimenti::Salumi	description for category and subcategory Alimenti::Salumi	
50	Alimenti::Spezie 	description for category and subcategory Alimenti::Spezie 	
51	Alimenti::Uova	description for category and subcategory Alimenti::Uova	
52	Alimenti::Verdura	description for category and subcategory Alimenti::Verdura	
53	Detergenti	description for category and subcategory Detergenti	
54	Igiene casa 	description for category and subcategory Igiene casa 	
55	Industria::Carta 	description for category and subcategory Industria::Carta 	
56	Piante 	description for category and subcategory Piante 	
57	Piante::Piante aromatiche 	description for category and subcategory Piante::Piante aromatiche 	
58	Alimenti::Dolci	description for category and subcategory Alimenti::Dolci	
6	Abbigliamento::Calzature::Calzature uomo 	description for category and subcategory Abbigliamento::Calzature::Calzature uomo 	
7	Abbigliamento::Vestiario 	description for category and subcategory Abbigliamento::Vestiario 	
8	Abbigliamento::Vestiario::Vestiario bambino 	description for category and subcategory Abbigliamento::Vestiario::Vestiario bambino 	
9	Abbigliamento::Vestiario::Vestiario donna 	description for category and subcategory Abbigliamento::Vestiario::Vestiario donna 	
10	Abbigliamento::Vestiario::Vestiario uomo 	description for category and subcategory Abbigliamento::Vestiario::Vestiario uomo 	
12	Alimenti::Bevande 	description for category and subcategory Alimenti::Bevande 	
13	Alimenti::Bevande::Analcoliche 	description for category and subcategory Alimenti::Bevande::Analcoliche 	
2	Abbigliamento::Calzature 	description for category and subcategory Abbigliamento::Calzature 	
3	Abbigliamento::Calzature::Calzature accessori 	description for category and subcategory Abbigliamento::Calzature::Calzature accessori 	
4	Abbigliamento::Calzature::Calzature bambino 	description for category and subcategory Abbigliamento::Calzature::Calzature bambino 	
5	Abbigliamento::Calzature::Calzature donna 	description for category and subcategory Abbigliamento::Calzature::Calzature donna 	
69	Alimenti::Carne::Rossa::Pecora	description for category and subcategory Alimenti::Carne::Rossa::Pecora	
70	Alimenti::Carne::Rossa::Vitello 	description for category and subcategory Alimenti::Carne::Rossa::Vitello 	
71	Alimenti::Formaggi e latticini::Mucca 	description for category and subcategory Alimenti::Formaggi e latticini::Mucca 	
72	Alimenti::Formaggi e latticini::Pecora 	description for category and subcategory Alimenti::Formaggi e latticini::Pecora 	
73	Alimenti::Cereali	description for category and subcategory Alimenti::Cereali	
74	Alimenti::Pesce::Mare	description for category and subcategory Alimenti::Pesce::Mare	
75	Alimenti::Pesce::Fiume	description for category and subcategory Alimenti::Pesce::Fiume	
76	Cosmesi	description for category and subcategory Cosmesi	
77	Cosmesi::Shampoo e Dentifricio	description for category and subcategory Cosmesi::Shampoo e Dentifricio	
78	Cosmesi::Saponi e Detergenti intimi	description for category and subcategory Cosmesi::Saponi e Detergenti intimi	
79	Cosmesi::Olii, crème e uguenti	description for category and subcategory Cosmesi::Olii, crème e uguenti	
80	Cosmesi::Barba	description for category and subcategory Cosmesi::Barba	
81	Non definita	nessuna categoria definita per questo prodotto	
59	Alimenti::Dolci::Zucchero	description for category and subcategory Alimenti::Dolci::Zucchero	
60	Edilizia	description for category and subcategory Edilizia	
61	Alimenti::Gelato	description for category and subcategory Alimenti::Gelato	
62	Alimenti::Farine	description for category and subcategory Alimenti::Farine	
63	Alimenti::Bevande::Tè::Tè nero	description for category and subcategory Alimenti::Bevande::Tè::Tè nero	
64	Alimenti::Bevande::Tè::Tè verde	description for category and subcategory Alimenti::Bevande::Tè::Tè verde	
65	Alimenti::Carne::Bianca::Coniglio 	description for category and subcategory Alimenti::Carne::Bianca::Coniglio 	
66	Alimenti::Carne::Bianca::Pollame 	description for category and subcategory Alimenti::Carne::Bianca::Pollame 	
67	Alimenti::Formaggi e latticini::Capra 	description for category and subcategory Alimenti::Formaggi e latticini::Capra 	
68	Alimenti::Carne::Rossa::Maiale 	description for category and subcategory Alimenti::Carne::Rossa::Maiale 	
\.


--
-- Name: supplier_productcategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_productcategory_id_seq', 81, true);


--
-- Data for Name: supplier_productmu; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_productmu (id, name, symbol) FROM stdin;
1	Millilitro	Ml
2	Centilitro	Cl
3	Decilitro	Dl
4	Litro	Lt
5	Grammo	Gr
6	Etto	Hg
7	Kilo	Kg
\.


--
-- Name: supplier_productmu_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_productmu_id_seq', 7, true);


--
-- Data for Name: supplier_productpu; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_productpu (id, name, symbol, description) FROM stdin;
17	Paio	paio	
1	Bottiglia	BTL	description for Bottiglia [BTL]
2	Cartone	BOX	description for Cartone [BOX]
3	Cassa	CX	description for Cassa [CX ]
5	Confezione	CF	description for Confezione [Cf ]
6	Dama	DAM	description for Dama [DAM]
9	Fila	PAN	description for Fila [PAN]
10	Forma	FOR	description for Forma [FOR]
15	Pacco	PAC	description for Pacco [PAC]
16	Pezzo	PZ	description for Pezzo [PZ ]
\.


--
-- Name: supplier_productpu_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_productpu_id_seq', 17, true);


--
-- Data for Name: supplier_supplier; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_supplier (id, name, seat_id, vat_number, ssn, website, frontman_id, flavour, n_employers, logo, iban, description) FROM stdin;
2	Fornitore 02	2	\N	\N		7	COMPANY	\N			
5	Generico	\N	\N	\N		6	COMPANY	\N			
6	nuovo	\N	\N	\N		7	COMPANY	\N			
1	Fornitore 01	1	\N	\N		6	COMPANY	\N	images/supplier/2014-04-1397389397-fornitore-01-icon.png		
4	Alchemia	16	0000	\N		30	COOPERATING	\N	images/supplier/2014-05-1399139166-alchemia-icon.gif		
3	Pasta Demo	3	\N	\N		23	COMPANY	\N			
\.


--
-- Data for Name: supplier_supplier_certifications; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_supplier_certifications (id, supplier_id, certification_id) FROM stdin;
3	2	1
19	1	1
21	4	5
22	3	1
23	3	2
24	3	5
25	3	7
\.


--
-- Name: supplier_supplier_certifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_supplier_certifications_id_seq', 25, true);


--
-- Data for Name: supplier_supplier_contact_set; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_supplier_contact_set (id, supplier_id, contact_id) FROM stdin;
14	5	51
15	5	52
16	6	53
17	6	54
19	1	49
\.


--
-- Name: supplier_supplier_contact_set_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_supplier_contact_set_id_seq', 21, true);


--
-- Name: supplier_supplier_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_supplier_id_seq', 6, true);


--
-- Data for Name: supplier_supplieragent; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_supplieragent (id, supplier_id, person_id, job_title, job_description) FROM stdin;
\.


--
-- Name: supplier_supplieragent_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_supplieragent_id_seq', 1, false);


--
-- Data for Name: supplier_supplierconfig; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_supplierconfig (id, supplier_id, receive_order_via_email_on_finalize, use_custom_categories) FROM stdin;
2	2	t	f
3	3	t	f
4	4	t	f
1	1	t	f
5	5	t	f
6	6	t	f
\.


--
-- Name: supplier_supplierconfig_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_supplierconfig_id_seq', 6, true);


--
-- Data for Name: supplier_supplierconfig_products_made_by_set; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_supplierconfig_products_made_by_set (id, supplierconfig_id, supplier_id) FROM stdin;
1	1	1
2	2	2
3	3	3
4	4	4
5	5	5
6	6	6
\.


--
-- Name: supplier_supplierconfig_products_made_by_set_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_supplierconfig_products_made_by_set_id_seq', 6, true);


--
-- Data for Name: supplier_supplierproductcategory; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_supplierproductcategory (id, supplier_id, name, sorting) FROM stdin;
\.


--
-- Name: supplier_supplierproductcategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_supplierproductcategory_id_seq', 1, false);


--
-- Data for Name: supplier_supplierstock; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_supplierstock (id, supplier_id, product_id, supplier_category_id, image, price, code, amount_available, units_minimum_amount, units_per_box, detail_minimum_amount, detail_step, delivery_notes, deleted) FROM stdin;
3	1	3	\N		10.0000	\N	1000000000	1	1.00	1.00	1.00		f
4	2	4	\N		40.0000	\N	1000000000	1	1.00	1.00	1.00		f
5	2	5	\N		50.0000	\N	1000000000	1	1.00	1.00	1.00		f
1	1	1	\N		20.0000	\N	1000000000	1	1.00	1.00	1.00		f
2	1	2	\N		25.0000	\N	1000000000	1	1.00	1.00	1.00		f
6	1	6	\N		3.5000	010ORC	1000000000	1	12.00	1.00	1.00		f
7	3	7	\N		2.5000	001SPA	1000000000	1	20.00	1.00	1.00		f
10	3	10	\N		4.0000	001FUS	1000000000	1	12.00	1.00	1.00		f
9	3	9	\N		3.2500	001PEN	1000000000	1	12.00	1.00	1.00		f
8	3	8	\N		3.0000	001LIN	1000000000	1	20.00	1.00	1.00		f
11	3	11	\N		4.5000	001FIL	1000000000	1	12.00	1.00	1.00		f
12	3	12	\N		4.5000	012SPA	1000000000	1	20.00	1.00	1.00		f
13	3	13	\N		4.0000	012LIN	1000000000	1	20.00	1.00	1.00		f
14	3	14	\N		5.0000	012PEN	1000000000	1	12.00	1.00	1.00		f
15	3	15	\N		5.5000	012FUS	1000000000	1	12.00	1.00	1.00		f
16	3	16	\N		6.0000	012TRE	1000000000	1	12.00	1.00	1.00		f
17	3	17	\N		2.5600	018SPA	1000000000	20	1.00	1.00	1.00		f
18	4	18	\N		200.0000	\N	1000000000	1	1.00	1.00	1.00		f
19	4	19	\N		20.0000	\N	1000000000	1	1.00	1.00	1.00		f
20	3	20	\N		2.0000	\N	1000000000	1	12.00	4.00	2.00		f
\.


--
-- Name: supplier_supplierstock_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_supplierstock_id_seq', 20, true);


--
-- Data for Name: supplier_unitsconversion; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY supplier_unitsconversion (id, src_id, dst_id, amount) FROM stdin;
4	2	2	1.0000
5	2	3	0.1000
6	2	4	0.0100
7	2	1	10.0000
8	3	2	10.0000
14	3	3	1.0000
9	3	4	0.1000
10	3	1	100.0000
15	6	6	1.0000
11	6	5	100.0000
12	6	7	0.1000
13	5	6	0.0100
16	5	5	1.0000
1	5	7	0.0010
19	7	6	10.0000
2	7	5	1000.0000
3	7	7	1.0000
20	4	2	100.0000
21	4	6	10.0000
17	4	4	1.0000
22	4	1	1000.0000
23	1	2	0.1000
24	1	3	0.0100
25	1	4	0.0010
18	1	1	1.0000
\.


--
-- Name: supplier_unitsconversion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('supplier_unitsconversion_id_seq', 25, true);


--
-- Data for Name: users_userprofile; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY users_userprofile (id, user_id, default_role_id) FROM stdin;
1	1	1
3	3	2
4	4	5
5	5	5
16	16	17
18	18	2
20	20	2
21	21	2
22	22	22
23	23	25
27	32	35
28	33	35
2	2	43
29	34	2
31	36	8
32	37	4
\.


--
-- Name: users_userprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('users_userprofile_id_seq', 32, true);


--
-- Data for Name: workflows_state; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY workflows_state (id, name, workflow_id) FROM stdin;
1	Prepared	1
2	Open	1
3	Closed	1
4	Unpaid	1
5	Archived	1
6	Canceled	1
7	Open	2
8	Closed	2
9	On completion	2
10	Finalized	2
11	Sent	2
12	Delivered	2
13	Archived	2
14	Canceled	2
15	Unconfirmed	3
16	Confirmed	3
17	Finalized	3
18	Sent	3
19	Ready for withdraw	3
20	Withdrawn	3
21	Not withdrawn	3
22	Canceled	3
\.


--
-- Name: workflows_state_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('workflows_state_id_seq', 22, true);


--
-- Data for Name: workflows_state_transitions; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY workflows_state_transitions (id, state_id, transition_id) FROM stdin;
1	1	1
2	2	2
3	2	3
4	3	4
5	3	5
6	4	4
7	2	6
8	3	6
9	1	6
10	7	7
11	8	8
12	8	11
13	8	9
14	9	10
15	10	12
16	11	13
17	12	14
18	7	15
19	8	15
20	9	15
21	10	15
22	11	15
23	15	16
24	16	17
25	16	18
26	17	19
27	18	20
28	19	21
29	19	22
30	16	23
31	17	23
32	18	23
\.


--
-- Name: workflows_state_transitions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('workflows_state_transitions_id_seq', 32, true);


--
-- Data for Name: workflows_stateinheritanceblock; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY workflows_stateinheritanceblock (id, state_id, permission_id) FROM stdin;
\.


--
-- Name: workflows_stateinheritanceblock_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('workflows_stateinheritanceblock_id_seq', 1, false);


--
-- Data for Name: workflows_stateobjectrelation; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY workflows_stateobjectrelation (id, content_type_id, content_id, state_id) FROM stdin;
52	90	44	3
3	94	\N	15
61	90	46	4
64	90	47	4
6	94	1	15
7	94	2	15
8	94	3	15
9	94	8	15
10	94	9	15
68	90	49	3
67	90	48	5
11	94	7	15
69	90	50	4
1	90	1	5
5	90	4	5
2	90	2	5
4	90	3	5
70	90	51	5
12	90	5	5
73	90	54	3
71	90	52	3
72	90	53	3
45	94	31	15
76	94	95	15
77	94	96	15
78	94	111	15
74	90	55	5
75	90	56	3
81	94	113	15
82	94	114	15
83	94	115	15
46	90	38	3
84	94	116	15
79	90	57	3
80	90	58	3
47	90	39	5
48	90	40	5
41	90	34	3
42	90	35	3
43	90	36	3
54	94	59	15
55	94	60	15
56	94	61	15
57	94	62	15
58	94	63	15
59	94	64	15
60	94	65	15
62	94	67	15
63	94	68	15
65	94	66	15
66	94	72	15
53	90	45	3
51	90	43	3
49	90	41	3
50	90	42	3
44	90	37	4
85	90	59	3
\.


--
-- Name: workflows_stateobjectrelation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('workflows_stateobjectrelation_id_seq', 85, true);


--
-- Data for Name: workflows_statepermissionrelation; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY workflows_statepermissionrelation (id, state_id, permission_id, role_id) FROM stdin;
\.


--
-- Name: workflows_statepermissionrelation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('workflows_statepermissionrelation_id_seq', 1, false);


--
-- Data for Name: workflows_transition; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY workflows_transition (id, name, workflow_id, destination_id, condition, permission_id) FROM stdin;
1	Open	1	2		\N
2	Close	1	3		\N
3	Close and send	1	3		\N
4	Archive	1	5		\N
5	MAKE UNPAID	1	4		\N
6	Cancel	1	6		\N
7	Close	2	8		\N
8	Reopen	2	7		\N
9	Start completion	2	9		\N
10	End completion	2	8		\N
11	Finalize	2	10		\N
12	Send	2	11		\N
13	Set delivered	2	12		\N
14	Archive	2	13		\N
15	Cancel	2	14		\N
16	Confirm	3	16		\N
17	Unconfirm	3	15		\N
18	Finalize	3	17		\N
19	Send	3	18		\N
20	Make ready	3	19		\N
21	Set withdrawn	3	20		\N
22	Set not withdrawn	3	21		\N
23	Cancel	3	22		\N
\.


--
-- Name: workflows_transition_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('workflows_transition_id_seq', 23, true);


--
-- Data for Name: workflows_workflow; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY workflows_workflow (id, name, initial_state_id) FROM stdin;
1	SimpleSupplierOrderDefault	1
2	SupplierOrderDefault	7
3	GASMemberOrderDefault	15
\.


--
-- Name: workflows_workflow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('workflows_workflow_id_seq', 3, true);


--
-- Data for Name: workflows_workflowmodelrelation; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY workflows_workflowmodelrelation (id, content_type_id, workflow_id) FROM stdin;
\.


--
-- Name: workflows_workflowmodelrelation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('workflows_workflowmodelrelation_id_seq', 1, false);


--
-- Data for Name: workflows_workflowobjectrelation; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY workflows_workflowobjectrelation (id, content_type_id, content_id, workflow_id) FROM stdin;
1	90	1	1
2	90	2	1
3	94	\N	3
4	90	3	1
5	90	4	1
6	94	1	3
7	94	2	3
8	94	3	3
9	94	8	3
10	94	9	3
11	94	7	3
12	90	5	1
41	90	34	1
42	90	35	1
43	90	36	1
44	90	37	1
45	94	31	3
46	90	38	1
47	90	39	1
48	90	40	1
49	90	41	1
50	90	42	1
51	90	43	1
52	90	44	1
53	90	45	1
54	94	59	3
55	94	60	3
56	94	61	3
57	94	62	3
58	94	63	3
59	94	64	3
60	94	65	3
61	90	46	1
62	94	67	3
63	94	68	3
64	90	47	1
65	94	66	3
66	94	72	3
67	90	48	1
68	90	49	1
69	90	50	1
70	90	51	1
71	90	52	1
72	90	53	1
73	90	54	1
74	90	55	1
75	90	56	1
76	94	95	3
77	94	96	3
78	94	111	3
79	90	57	1
80	90	58	1
81	94	113	3
82	94	114	3
83	94	115	3
84	94	116	3
85	90	59	1
\.


--
-- Name: workflows_workflowobjectrelation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('workflows_workflowobjectrelation_id_seq', 85, true);


--
-- Data for Name: workflows_workflowpermissionrelation; Type: TABLE DATA; Schema: public; Owner: gf_stage
--

COPY workflows_workflowpermissionrelation (id, workflow_id, permission_id) FROM stdin;
\.


--
-- Name: workflows_workflowpermissionrelation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: gf_stage
--

SELECT pg_catalog.setval('workflows_workflowpermissionrelation_id_seq', 1, false);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_message_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: base_contact_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY base_contact
    ADD CONSTRAINT base_contact_pkey PRIMARY KEY (id);


--
-- Name: base_defaulttransition_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY base_defaulttransition
    ADD CONSTRAINT base_defaulttransition_pkey PRIMARY KEY (id);


--
-- Name: base_historicalcontact_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY base_historicalcontact
    ADD CONSTRAINT base_historicalcontact_pkey PRIMARY KEY (history_id);


--
-- Name: base_historicaldefaulttransition_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY base_historicaldefaulttransition
    ADD CONSTRAINT base_historicaldefaulttransition_pkey PRIMARY KEY (history_id);


--
-- Name: base_historicalperson_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY base_historicalperson
    ADD CONSTRAINT base_historicalperson_pkey PRIMARY KEY (history_id);


--
-- Name: base_historicalplace_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY base_historicalplace
    ADD CONSTRAINT base_historicalplace_pkey PRIMARY KEY (history_id);


--
-- Name: base_person_contact_set_person_id_contact_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY base_person_contact_set
    ADD CONSTRAINT base_person_contact_set_person_id_contact_id_key UNIQUE (person_id, contact_id);


--
-- Name: base_person_contact_set_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY base_person_contact_set
    ADD CONSTRAINT base_person_contact_set_pkey PRIMARY KEY (id);


--
-- Name: base_person_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY base_person
    ADD CONSTRAINT base_person_pkey PRIMARY KEY (id);


--
-- Name: base_person_ssn_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY base_person
    ADD CONSTRAINT base_person_ssn_key UNIQUE (ssn);


--
-- Name: base_person_user_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY base_person
    ADD CONSTRAINT base_person_user_id_key UNIQUE (user_id);


--
-- Name: base_place_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY base_place
    ADD CONSTRAINT base_place_pkey PRIMARY KEY (id);


--
-- Name: blockconfiguration_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY blockconfiguration
    ADD CONSTRAINT blockconfiguration_pkey PRIMARY KEY (id);


--
-- Name: captcha_captchastore_hashkey_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY captcha_captchastore
    ADD CONSTRAINT captcha_captchastore_hashkey_key UNIQUE (hashkey);


--
-- Name: captcha_captchastore_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY captcha_captchastore
    ADD CONSTRAINT captcha_captchastore_pkey PRIMARY KEY (id);


--
-- Name: des_des_info_people_set_des_id_person_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY des_des_info_people_set
    ADD CONSTRAINT des_des_info_people_set_des_id_person_id_key UNIQUE (des_id, person_id);


--
-- Name: des_des_info_people_set_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY des_des_info_people_set
    ADD CONSTRAINT des_des_info_people_set_pkey PRIMARY KEY (id);


--
-- Name: des_des_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY des_des
    ADD CONSTRAINT des_des_pkey PRIMARY KEY (site_ptr_id);


--
-- Name: des_siteattr_name_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY des_siteattr
    ADD CONSTRAINT des_siteattr_name_key UNIQUE (name);


--
-- Name: des_siteattr_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY des_siteattr
    ADD CONSTRAINT des_siteattr_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_comment_flags_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY django_comment_flags
    ADD CONSTRAINT django_comment_flags_pkey PRIMARY KEY (id);


--
-- Name: django_comment_flags_user_id_comment_id_flag_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY django_comment_flags
    ADD CONSTRAINT django_comment_flags_user_id_comment_id_flag_key UNIQUE (user_id, comment_id, flag);


--
-- Name: django_comments_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY django_comments
    ADD CONSTRAINT django_comments_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_model_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_key UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: flexi_auth_param_name_content_type_id_object_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY flexi_auth_param
    ADD CONSTRAINT flexi_auth_param_name_content_type_id_object_id_key UNIQUE (name, content_type_id, object_id);


--
-- Name: flexi_auth_param_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY flexi_auth_param
    ADD CONSTRAINT flexi_auth_param_pkey PRIMARY KEY (id);


--
-- Name: flexi_auth_paramrole_param_set_paramrole_id_param_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY flexi_auth_paramrole_param_set
    ADD CONSTRAINT flexi_auth_paramrole_param_set_paramrole_id_param_id_key UNIQUE (paramrole_id, param_id);


--
-- Name: flexi_auth_paramrole_param_set_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY flexi_auth_paramrole_param_set
    ADD CONSTRAINT flexi_auth_paramrole_param_set_pkey PRIMARY KEY (id);


--
-- Name: flexi_auth_paramrole_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY flexi_auth_paramrole
    ADD CONSTRAINT flexi_auth_paramrole_pkey PRIMARY KEY (id);


--
-- Name: flexi_auth_principalparamrolerelation_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY flexi_auth_principalparamrolerelation
    ADD CONSTRAINT flexi_auth_principalparamrolerelation_pkey PRIMARY KEY (id);


--
-- Name: gas_delivery_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_delivery
    ADD CONSTRAINT gas_delivery_pkey PRIMARY KEY (id);


--
-- Name: gas_gas_contact_set_gas_id_6e974dfd_uniq; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gas_contact_set
    ADD CONSTRAINT gas_gas_contact_set_gas_id_6e974dfd_uniq UNIQUE (gas_id, contact_id);


--
-- Name: gas_gas_contact_set_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gas_contact_set
    ADD CONSTRAINT gas_gas_contact_set_pkey PRIMARY KEY (id);


--
-- Name: gas_gas_id_in_des_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gas
    ADD CONSTRAINT gas_gas_id_in_des_key UNIQUE (id_in_des);


--
-- Name: gas_gas_name_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gas
    ADD CONSTRAINT gas_gas_name_key UNIQUE (name);


--
-- Name: gas_gas_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gas
    ADD CONSTRAINT gas_gas_pkey PRIMARY KEY (id);


--
-- Name: gas_gasactivist_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gasactivist
    ADD CONSTRAINT gas_gasactivist_pkey PRIMARY KEY (id);


--
-- Name: gas_gasconfig_gas_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gasconfig
    ADD CONSTRAINT gas_gasconfig_gas_id_key UNIQUE (gas_id);


--
-- Name: gas_gasconfig_intergas_connection_set_gasconfig_id_1403d4c_uniq; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gasconfig_intergas_connection_set
    ADD CONSTRAINT gas_gasconfig_intergas_connection_set_gasconfig_id_1403d4c_uniq UNIQUE (gasconfig_id, gas_id);


--
-- Name: gas_gasconfig_intergas_connection_set_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gasconfig_intergas_connection_set
    ADD CONSTRAINT gas_gasconfig_intergas_connection_set_pkey PRIMARY KEY (id);


--
-- Name: gas_gasconfig_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gasconfig
    ADD CONSTRAINT gas_gasconfig_pkey PRIMARY KEY (id);


--
-- Name: gas_gasmember_available_for_roles_gasmember_id_56ff009a_uniq; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gasmember_available_for_roles
    ADD CONSTRAINT gas_gasmember_available_for_roles_gasmember_id_56ff009a_uniq UNIQUE (gasmember_id, role_id);


--
-- Name: gas_gasmember_available_for_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gasmember_available_for_roles
    ADD CONSTRAINT gas_gasmember_available_for_roles_pkey PRIMARY KEY (id);


--
-- Name: gas_gasmember_gas_id_318fda9b_uniq; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gasmember
    ADD CONSTRAINT gas_gasmember_gas_id_318fda9b_uniq UNIQUE (gas_id, id_in_gas);


--
-- Name: gas_gasmember_person_id_314d8113_uniq; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gasmember
    ADD CONSTRAINT gas_gasmember_person_id_314d8113_uniq UNIQUE (person_id, gas_id);


--
-- Name: gas_gasmember_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gasmember
    ADD CONSTRAINT gas_gasmember_pkey PRIMARY KEY (id);


--
-- Name: gas_gasmemberorder_ordered_product_id_140471bf_uniq; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gasmemberorder
    ADD CONSTRAINT gas_gasmemberorder_ordered_product_id_140471bf_uniq UNIQUE (ordered_product_id, purchaser_id);


--
-- Name: gas_gasmemberorder_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gasmemberorder
    ADD CONSTRAINT gas_gasmemberorder_pkey PRIMARY KEY (id);


--
-- Name: gas_gassupplierorder_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gassupplierorder
    ADD CONSTRAINT gas_gassupplierorder_pkey PRIMARY KEY (id);


--
-- Name: gas_gassupplierorderproduct_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gassupplierorderproduct
    ADD CONSTRAINT gas_gassupplierorderproduct_pkey PRIMARY KEY (id);


--
-- Name: gas_gassuppliersolidalpact_gas_id_609886cb_uniq; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gassuppliersolidalpact
    ADD CONSTRAINT gas_gassuppliersolidalpact_gas_id_609886cb_uniq UNIQUE (gas_id, supplier_id);


--
-- Name: gas_gassuppliersolidalpact_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gassuppliersolidalpact
    ADD CONSTRAINT gas_gassuppliersolidalpact_pkey PRIMARY KEY (id);


--
-- Name: gas_gassupplierstock_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_gassupplierstock
    ADD CONSTRAINT gas_gassupplierstock_pkey PRIMARY KEY (id);


--
-- Name: gas_historicaldelivery_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_historicaldelivery
    ADD CONSTRAINT gas_historicaldelivery_pkey PRIMARY KEY (history_id);


--
-- Name: gas_historicalgas_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_historicalgas
    ADD CONSTRAINT gas_historicalgas_pkey PRIMARY KEY (history_id);


--
-- Name: gas_historicalgasactivist_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_historicalgasactivist
    ADD CONSTRAINT gas_historicalgasactivist_pkey PRIMARY KEY (history_id);


--
-- Name: gas_historicalgasconfig_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_historicalgasconfig
    ADD CONSTRAINT gas_historicalgasconfig_pkey PRIMARY KEY (history_id);


--
-- Name: gas_historicalgasmember_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_historicalgasmember
    ADD CONSTRAINT gas_historicalgasmember_pkey PRIMARY KEY (history_id);


--
-- Name: gas_historicalgasmemberorder_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_historicalgasmemberorder
    ADD CONSTRAINT gas_historicalgasmemberorder_pkey PRIMARY KEY (history_id);


--
-- Name: gas_historicalgassupplierorder_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_historicalgassupplierorder
    ADD CONSTRAINT gas_historicalgassupplierorder_pkey PRIMARY KEY (history_id);


--
-- Name: gas_historicalgassupplierorderproduct_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_historicalgassupplierorderproduct
    ADD CONSTRAINT gas_historicalgassupplierorderproduct_pkey PRIMARY KEY (history_id);


--
-- Name: gas_historicalgassuppliersolidalpact_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_historicalgassuppliersolidalpact
    ADD CONSTRAINT gas_historicalgassuppliersolidalpact_pkey PRIMARY KEY (history_id);


--
-- Name: gas_historicalgassupplierstock_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_historicalgassupplierstock
    ADD CONSTRAINT gas_historicalgassupplierstock_pkey PRIMARY KEY (history_id);


--
-- Name: gas_historicalwithdrawal_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_historicalwithdrawal
    ADD CONSTRAINT gas_historicalwithdrawal_pkey PRIMARY KEY (history_id);


--
-- Name: gas_withdrawal_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY gas_withdrawal
    ADD CONSTRAINT gas_withdrawal_pkey PRIMARY KEY (id);


--
-- Name: notification_notice_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY notification_notice
    ADD CONSTRAINT notification_notice_pkey PRIMARY KEY (id);


--
-- Name: notification_noticequeuebatch_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY notification_noticequeuebatch
    ADD CONSTRAINT notification_noticequeuebatch_pkey PRIMARY KEY (id);


--
-- Name: notification_noticesetting_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY notification_noticesetting
    ADD CONSTRAINT notification_noticesetting_pkey PRIMARY KEY (id);


--
-- Name: notification_noticesetting_user_id_notice_type_id_medium_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY notification_noticesetting
    ADD CONSTRAINT notification_noticesetting_user_id_notice_type_id_medium_key UNIQUE (user_id, notice_type_id, medium);


--
-- Name: notification_noticetype_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY notification_noticetype
    ADD CONSTRAINT notification_noticetype_pkey PRIMARY KEY (id);


--
-- Name: notification_observeditem_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY notification_observeditem
    ADD CONSTRAINT notification_observeditem_pkey PRIMARY KEY (id);


--
-- Name: permissions_objectpermission_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY permissions_objectpermission
    ADD CONSTRAINT permissions_objectpermission_pkey PRIMARY KEY (id);


--
-- Name: permissions_objectpermissioninheritanceblock_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY permissions_objectpermissioninheritanceblock
    ADD CONSTRAINT permissions_objectpermissioninheritanceblock_pkey PRIMARY KEY (id);


--
-- Name: permissions_permission_codename_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY permissions_permission
    ADD CONSTRAINT permissions_permission_codename_key UNIQUE (codename);


--
-- Name: permissions_permission_content_permission_id_contenttype_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY permissions_permission_content_types
    ADD CONSTRAINT permissions_permission_content_permission_id_contenttype_id_key UNIQUE (permission_id, contenttype_id);


--
-- Name: permissions_permission_content_types_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY permissions_permission_content_types
    ADD CONSTRAINT permissions_permission_content_types_pkey PRIMARY KEY (id);


--
-- Name: permissions_permission_name_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY permissions_permission
    ADD CONSTRAINT permissions_permission_name_key UNIQUE (name);


--
-- Name: permissions_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY permissions_permission
    ADD CONSTRAINT permissions_permission_pkey PRIMARY KEY (id);


--
-- Name: permissions_principalrolerelation_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY permissions_principalrolerelation
    ADD CONSTRAINT permissions_principalrolerelation_pkey PRIMARY KEY (id);


--
-- Name: permissions_role_name_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY permissions_role
    ADD CONSTRAINT permissions_role_name_key UNIQUE (name);


--
-- Name: permissions_role_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY permissions_role
    ADD CONSTRAINT permissions_role_pkey PRIMARY KEY (id);


--
-- Name: registration_registrationprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY registration_registrationprofile
    ADD CONSTRAINT registration_registrationprofile_pkey PRIMARY KEY (id);


--
-- Name: registration_registrationprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY registration_registrationprofile
    ADD CONSTRAINT registration_registrationprofile_user_id_key UNIQUE (user_id);


--
-- Name: rest_homepage_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY rest_homepage
    ADD CONSTRAINT rest_homepage_pkey PRIMARY KEY (id);


--
-- Name: rest_page_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY rest_page
    ADD CONSTRAINT rest_page_pkey PRIMARY KEY (id);


--
-- Name: simple_accounting_account_parent_id_name_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY simple_accounting_account
    ADD CONSTRAINT simple_accounting_account_parent_id_name_key UNIQUE (parent_id, name);


--
-- Name: simple_accounting_account_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY simple_accounting_account
    ADD CONSTRAINT simple_accounting_account_pkey PRIMARY KEY (id);


--
-- Name: simple_accounting_accountsystem_owner_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY simple_accounting_accountsystem
    ADD CONSTRAINT simple_accounting_accountsystem_owner_id_key UNIQUE (owner_id);


--
-- Name: simple_accounting_accountsystem_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY simple_accounting_accountsystem
    ADD CONSTRAINT simple_accounting_accountsystem_pkey PRIMARY KEY (id);


--
-- Name: simple_accounting_accounttype_name_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY simple_accounting_accounttype
    ADD CONSTRAINT simple_accounting_accounttype_name_key UNIQUE (name);


--
-- Name: simple_accounting_accounttype_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY simple_accounting_accounttype
    ADD CONSTRAINT simple_accounting_accounttype_pkey PRIMARY KEY (id);


--
-- Name: simple_accounting_cashflow_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY simple_accounting_cashflow
    ADD CONSTRAINT simple_accounting_cashflow_pkey PRIMARY KEY (id);


--
-- Name: simple_accounting_invoice_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY simple_accounting_invoice
    ADD CONSTRAINT simple_accounting_invoice_pkey PRIMARY KEY (id);


--
-- Name: simple_accounting_ledgerentry_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY simple_accounting_ledgerentry
    ADD CONSTRAINT simple_accounting_ledgerentry_pkey PRIMARY KEY (id);


--
-- Name: simple_accounting_split_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY simple_accounting_split
    ADD CONSTRAINT simple_accounting_split_pkey PRIMARY KEY (id);


--
-- Name: simple_accounting_subject_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY simple_accounting_subject
    ADD CONSTRAINT simple_accounting_subject_pkey PRIMARY KEY (id);


--
-- Name: simple_accounting_transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY simple_accounting_transaction
    ADD CONSTRAINT simple_accounting_transaction_pkey PRIMARY KEY (id);


--
-- Name: simple_accounting_transaction_split_set_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY simple_accounting_transaction_split_set
    ADD CONSTRAINT simple_accounting_transaction_split_set_pkey PRIMARY KEY (id);


--
-- Name: simple_accounting_transaction_split_transaction_id_split_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY simple_accounting_transaction_split_set
    ADD CONSTRAINT simple_accounting_transaction_split_transaction_id_split_id_key UNIQUE (transaction_id, split_id);


--
-- Name: simple_accounting_transaction_transaction_id_content_type_i_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY simple_accounting_transactionreference
    ADD CONSTRAINT simple_accounting_transaction_transaction_id_content_type_i_key UNIQUE (transaction_id, content_type_id, object_id);


--
-- Name: simple_accounting_transactionreference_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY simple_accounting_transactionreference
    ADD CONSTRAINT simple_accounting_transactionreference_pkey PRIMARY KEY (id);


--
-- Name: south_migrationhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY south_migrationhistory
    ADD CONSTRAINT south_migrationhistory_pkey PRIMARY KEY (id);


--
-- Name: supplier_certification_name_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_certification
    ADD CONSTRAINT supplier_certification_name_key UNIQUE (name);


--
-- Name: supplier_certification_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_certification
    ADD CONSTRAINT supplier_certification_pkey PRIMARY KEY (id);


--
-- Name: supplier_certification_symbol_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_certification
    ADD CONSTRAINT supplier_certification_symbol_key UNIQUE (symbol);


--
-- Name: supplier_historicalcertification_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_historicalcertification
    ADD CONSTRAINT supplier_historicalcertification_pkey PRIMARY KEY (history_id);


--
-- Name: supplier_historicalproduct_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_historicalproduct
    ADD CONSTRAINT supplier_historicalproduct_pkey PRIMARY KEY (history_id);


--
-- Name: supplier_historicalproductcategory_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_historicalproductcategory
    ADD CONSTRAINT supplier_historicalproductcategory_pkey PRIMARY KEY (history_id);


--
-- Name: supplier_historicalproductmu_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_historicalproductmu
    ADD CONSTRAINT supplier_historicalproductmu_pkey PRIMARY KEY (history_id);


--
-- Name: supplier_historicalproductpu_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_historicalproductpu
    ADD CONSTRAINT supplier_historicalproductpu_pkey PRIMARY KEY (history_id);


--
-- Name: supplier_historicalsupplier_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_historicalsupplier
    ADD CONSTRAINT supplier_historicalsupplier_pkey PRIMARY KEY (history_id);


--
-- Name: supplier_historicalsupplieragent_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_historicalsupplieragent
    ADD CONSTRAINT supplier_historicalsupplieragent_pkey PRIMARY KEY (history_id);


--
-- Name: supplier_historicalsupplierstock_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_historicalsupplierstock
    ADD CONSTRAINT supplier_historicalsupplierstock_pkey PRIMARY KEY (history_id);


--
-- Name: supplier_product_code_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_product
    ADD CONSTRAINT supplier_product_code_key UNIQUE (code);


--
-- Name: supplier_product_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_product
    ADD CONSTRAINT supplier_product_pkey PRIMARY KEY (id);


--
-- Name: supplier_productcategory_name_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_productcategory
    ADD CONSTRAINT supplier_productcategory_name_key UNIQUE (name);


--
-- Name: supplier_productcategory_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_productcategory
    ADD CONSTRAINT supplier_productcategory_pkey PRIMARY KEY (id);


--
-- Name: supplier_productmu_name_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_productmu
    ADD CONSTRAINT supplier_productmu_name_key UNIQUE (name);


--
-- Name: supplier_productmu_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_productmu
    ADD CONSTRAINT supplier_productmu_pkey PRIMARY KEY (id);


--
-- Name: supplier_productmu_symbol_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_productmu
    ADD CONSTRAINT supplier_productmu_symbol_key UNIQUE (symbol);


--
-- Name: supplier_productpu_name_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_productpu
    ADD CONSTRAINT supplier_productpu_name_key UNIQUE (name);


--
-- Name: supplier_productpu_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_productpu
    ADD CONSTRAINT supplier_productpu_pkey PRIMARY KEY (id);


--
-- Name: supplier_productpu_symbol_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_productpu
    ADD CONSTRAINT supplier_productpu_symbol_key UNIQUE (symbol);


--
-- Name: supplier_supplier_certificatio_supplier_id_certification_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_supplier_certifications
    ADD CONSTRAINT supplier_supplier_certificatio_supplier_id_certification_id_key UNIQUE (supplier_id, certification_id);


--
-- Name: supplier_supplier_certifications_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_supplier_certifications
    ADD CONSTRAINT supplier_supplier_certifications_pkey PRIMARY KEY (id);


--
-- Name: supplier_supplier_contact_set_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_supplier_contact_set
    ADD CONSTRAINT supplier_supplier_contact_set_pkey PRIMARY KEY (id);


--
-- Name: supplier_supplier_contact_set_supplier_id_contact_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_supplier_contact_set
    ADD CONSTRAINT supplier_supplier_contact_set_supplier_id_contact_id_key UNIQUE (supplier_id, contact_id);


--
-- Name: supplier_supplier_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_supplier
    ADD CONSTRAINT supplier_supplier_pkey PRIMARY KEY (id);


--
-- Name: supplier_supplier_ssn_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_supplier
    ADD CONSTRAINT supplier_supplier_ssn_key UNIQUE (ssn);


--
-- Name: supplier_supplier_vat_number_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_supplier
    ADD CONSTRAINT supplier_supplier_vat_number_key UNIQUE (vat_number);


--
-- Name: supplier_supplieragent_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_supplieragent
    ADD CONSTRAINT supplier_supplieragent_pkey PRIMARY KEY (id);


--
-- Name: supplier_supplierconfig_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_supplierconfig
    ADD CONSTRAINT supplier_supplierconfig_pkey PRIMARY KEY (id);


--
-- Name: supplier_supplierconfig_produ_supplierconfig_id_supplier_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_supplierconfig_products_made_by_set
    ADD CONSTRAINT supplier_supplierconfig_produ_supplierconfig_id_supplier_id_key UNIQUE (supplierconfig_id, supplier_id);


--
-- Name: supplier_supplierconfig_products_made_by_set_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_supplierconfig_products_made_by_set
    ADD CONSTRAINT supplier_supplierconfig_products_made_by_set_pkey PRIMARY KEY (id);


--
-- Name: supplier_supplierconfig_supplier_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_supplierconfig
    ADD CONSTRAINT supplier_supplierconfig_supplier_id_key UNIQUE (supplier_id);


--
-- Name: supplier_supplierproductcategory_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_supplierproductcategory
    ADD CONSTRAINT supplier_supplierproductcategory_pkey PRIMARY KEY (id);


--
-- Name: supplier_supplierstock_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_supplierstock
    ADD CONSTRAINT supplier_supplierstock_pkey PRIMARY KEY (id);


--
-- Name: supplier_unitsconversion_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_unitsconversion
    ADD CONSTRAINT supplier_unitsconversion_pkey PRIMARY KEY (id);


--
-- Name: supplier_unitsconversion_src_id_dst_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY supplier_unitsconversion
    ADD CONSTRAINT supplier_unitsconversion_src_id_dst_id_key UNIQUE (src_id, dst_id);


--
-- Name: users_userprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY users_userprofile
    ADD CONSTRAINT users_userprofile_pkey PRIMARY KEY (id);


--
-- Name: users_userprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY users_userprofile
    ADD CONSTRAINT users_userprofile_user_id_key UNIQUE (user_id);


--
-- Name: workflows_state_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY workflows_state
    ADD CONSTRAINT workflows_state_pkey PRIMARY KEY (id);


--
-- Name: workflows_state_transitions_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY workflows_state_transitions
    ADD CONSTRAINT workflows_state_transitions_pkey PRIMARY KEY (id);


--
-- Name: workflows_state_transitions_state_id_transition_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY workflows_state_transitions
    ADD CONSTRAINT workflows_state_transitions_state_id_transition_id_key UNIQUE (state_id, transition_id);


--
-- Name: workflows_stateinheritanceblock_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY workflows_stateinheritanceblock
    ADD CONSTRAINT workflows_stateinheritanceblock_pkey PRIMARY KEY (id);


--
-- Name: workflows_stateobjectrelation_content_type_id_content_id_st_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY workflows_stateobjectrelation
    ADD CONSTRAINT workflows_stateobjectrelation_content_type_id_content_id_st_key UNIQUE (content_type_id, content_id, state_id);


--
-- Name: workflows_stateobjectrelation_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY workflows_stateobjectrelation
    ADD CONSTRAINT workflows_stateobjectrelation_pkey PRIMARY KEY (id);


--
-- Name: workflows_statepermissionrelation_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY workflows_statepermissionrelation
    ADD CONSTRAINT workflows_statepermissionrelation_pkey PRIMARY KEY (id);


--
-- Name: workflows_transition_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY workflows_transition
    ADD CONSTRAINT workflows_transition_pkey PRIMARY KEY (id);


--
-- Name: workflows_workflow_name_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY workflows_workflow
    ADD CONSTRAINT workflows_workflow_name_key UNIQUE (name);


--
-- Name: workflows_workflow_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY workflows_workflow
    ADD CONSTRAINT workflows_workflow_pkey PRIMARY KEY (id);


--
-- Name: workflows_workflowmodelrelation_content_type_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY workflows_workflowmodelrelation
    ADD CONSTRAINT workflows_workflowmodelrelation_content_type_id_key UNIQUE (content_type_id);


--
-- Name: workflows_workflowmodelrelation_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY workflows_workflowmodelrelation
    ADD CONSTRAINT workflows_workflowmodelrelation_pkey PRIMARY KEY (id);


--
-- Name: workflows_workflowobjectrelation_content_type_id_content_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY workflows_workflowobjectrelation
    ADD CONSTRAINT workflows_workflowobjectrelation_content_type_id_content_id_key UNIQUE (content_type_id, content_id);


--
-- Name: workflows_workflowobjectrelation_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY workflows_workflowobjectrelation
    ADD CONSTRAINT workflows_workflowobjectrelation_pkey PRIMARY KEY (id);


--
-- Name: workflows_workflowpermissionrelat_workflow_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY workflows_workflowpermissionrelation
    ADD CONSTRAINT workflows_workflowpermissionrelat_workflow_id_permission_id_key UNIQUE (workflow_id, permission_id);


--
-- Name: workflows_workflowpermissionrelation_pkey; Type: CONSTRAINT; Schema: public; Owner: gf_stage; Tablespace: 
--

ALTER TABLE ONLY workflows_workflowpermissionrelation
    ADD CONSTRAINT workflows_workflowpermissionrelation_pkey PRIMARY KEY (id);


--
-- Name: auth_group_permissions_group_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX auth_group_permissions_group_id ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX auth_group_permissions_permission_id ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_message_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX auth_message_user_id ON auth_message USING btree (user_id);


--
-- Name: auth_permission_content_type_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX auth_permission_content_type_id ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX auth_user_groups_group_id ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX auth_user_groups_user_id ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_permission_id ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_user_id ON auth_user_user_permissions USING btree (user_id);


--
-- Name: base_defaulttransition_state_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_defaulttransition_state_id ON base_defaulttransition USING btree (state_id);


--
-- Name: base_defaulttransition_transition_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_defaulttransition_transition_id ON base_defaulttransition USING btree (transition_id);


--
-- Name: base_defaulttransition_workflow_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_defaulttransition_workflow_id ON base_defaulttransition USING btree (workflow_id);


--
-- Name: base_historicalcontact_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_historicalcontact_history_user_id ON base_historicalcontact USING btree (history_user_id);


--
-- Name: base_historicalcontact_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_historicalcontact_id ON base_historicalcontact USING btree (id);


--
-- Name: base_historicaldefaulttransition_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_historicaldefaulttransition_history_user_id ON base_historicaldefaulttransition USING btree (history_user_id);


--
-- Name: base_historicaldefaulttransition_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_historicaldefaulttransition_id ON base_historicaldefaulttransition USING btree (id);


--
-- Name: base_historicaldefaulttransition_state_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_historicaldefaulttransition_state_id ON base_historicaldefaulttransition USING btree (state_id);


--
-- Name: base_historicaldefaulttransition_transition_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_historicaldefaulttransition_transition_id ON base_historicaldefaulttransition USING btree (transition_id);


--
-- Name: base_historicaldefaulttransition_workflow_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_historicaldefaulttransition_workflow_id ON base_historicaldefaulttransition USING btree (workflow_id);


--
-- Name: base_historicalperson_address_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_historicalperson_address_id ON base_historicalperson USING btree (address_id);


--
-- Name: base_historicalperson_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_historicalperson_history_user_id ON base_historicalperson USING btree (history_user_id);


--
-- Name: base_historicalperson_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_historicalperson_id ON base_historicalperson USING btree (id);


--
-- Name: base_historicalperson_ssn; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_historicalperson_ssn ON base_historicalperson USING btree (ssn);


--
-- Name: base_historicalperson_ssn_like; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_historicalperson_ssn_like ON base_historicalperson USING btree (ssn varchar_pattern_ops);


--
-- Name: base_historicalperson_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_historicalperson_user_id ON base_historicalperson USING btree (user_id);


--
-- Name: base_historicalplace_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_historicalplace_history_user_id ON base_historicalplace USING btree (history_user_id);


--
-- Name: base_historicalplace_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_historicalplace_id ON base_historicalplace USING btree (id);


--
-- Name: base_person_address_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_person_address_id ON base_person USING btree (address_id);


--
-- Name: base_person_contact_set_contact_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_person_contact_set_contact_id ON base_person_contact_set USING btree (contact_id);


--
-- Name: base_person_contact_set_person_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX base_person_contact_set_person_id ON base_person_contact_set USING btree (person_id);


--
-- Name: blockconfiguration_blocktype; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX blockconfiguration_blocktype ON blockconfiguration USING btree (blocktype);


--
-- Name: blockconfiguration_blocktype_like; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX blockconfiguration_blocktype_like ON blockconfiguration USING btree (blocktype varchar_pattern_ops);


--
-- Name: blockconfiguration_resource_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX blockconfiguration_resource_id ON blockconfiguration USING btree (resource_id);


--
-- Name: blockconfiguration_resource_id_like; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX blockconfiguration_resource_id_like ON blockconfiguration USING btree (resource_id varchar_pattern_ops);


--
-- Name: blockconfiguration_resource_type; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX blockconfiguration_resource_type ON blockconfiguration USING btree (resource_type);


--
-- Name: blockconfiguration_resource_type_like; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX blockconfiguration_resource_type_like ON blockconfiguration USING btree (resource_type varchar_pattern_ops);


--
-- Name: blockconfiguration_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX blockconfiguration_user_id ON blockconfiguration USING btree (user_id);


--
-- Name: des_des_info_people_set_des_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX des_des_info_people_set_des_id ON des_des_info_people_set USING btree (des_id);


--
-- Name: des_des_info_people_set_person_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX des_des_info_people_set_person_id ON des_des_info_people_set USING btree (person_id);


--
-- Name: django_admin_log_content_type_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX django_admin_log_content_type_id ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX django_admin_log_user_id ON django_admin_log USING btree (user_id);


--
-- Name: django_comment_flags_comment_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX django_comment_flags_comment_id ON django_comment_flags USING btree (comment_id);


--
-- Name: django_comment_flags_flag; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX django_comment_flags_flag ON django_comment_flags USING btree (flag);


--
-- Name: django_comment_flags_flag_like; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX django_comment_flags_flag_like ON django_comment_flags USING btree (flag varchar_pattern_ops);


--
-- Name: django_comment_flags_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX django_comment_flags_user_id ON django_comment_flags USING btree (user_id);


--
-- Name: django_comments_content_type_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX django_comments_content_type_id ON django_comments USING btree (content_type_id);


--
-- Name: django_comments_site_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX django_comments_site_id ON django_comments USING btree (site_id);


--
-- Name: django_comments_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX django_comments_user_id ON django_comments USING btree (user_id);


--
-- Name: django_session_expire_date; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX django_session_expire_date ON django_session USING btree (expire_date);


--
-- Name: flexi_auth_param_content_type_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX flexi_auth_param_content_type_id ON flexi_auth_param USING btree (content_type_id);


--
-- Name: flexi_auth_paramrole_param_set_param_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX flexi_auth_paramrole_param_set_param_id ON flexi_auth_paramrole_param_set USING btree (param_id);


--
-- Name: flexi_auth_paramrole_param_set_paramrole_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX flexi_auth_paramrole_param_set_paramrole_id ON flexi_auth_paramrole_param_set USING btree (paramrole_id);


--
-- Name: flexi_auth_paramrole_role_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX flexi_auth_paramrole_role_id ON flexi_auth_paramrole USING btree (role_id);


--
-- Name: flexi_auth_principalparamrolerelation_group_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX flexi_auth_principalparamrolerelation_group_id ON flexi_auth_principalparamrolerelation USING btree (group_id);


--
-- Name: flexi_auth_principalparamrolerelation_role_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX flexi_auth_principalparamrolerelation_role_id ON flexi_auth_principalparamrolerelation USING btree (role_id);


--
-- Name: flexi_auth_principalparamrolerelation_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX flexi_auth_principalparamrolerelation_user_id ON flexi_auth_principalparamrolerelation USING btree (user_id);


--
-- Name: gas_delivery_place_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_delivery_place_id ON gas_delivery USING btree (place_id);


--
-- Name: gas_gas_contact_set_contact_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gas_contact_set_contact_id ON gas_gas_contact_set USING btree (contact_id);


--
-- Name: gas_gas_contact_set_gas_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gas_contact_set_gas_id ON gas_gas_contact_set USING btree (gas_id);


--
-- Name: gas_gas_des_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gas_des_id ON gas_gas USING btree (des_id);


--
-- Name: gas_gas_headquarter_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gas_headquarter_id ON gas_gas USING btree (headquarter_id);


--
-- Name: gas_gas_orders_email_contact_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gas_orders_email_contact_id ON gas_gas USING btree (orders_email_contact_id);


--
-- Name: gas_gasactivist_gas_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gasactivist_gas_id ON gas_gasactivist USING btree (gas_id);


--
-- Name: gas_gasactivist_person_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gasactivist_person_id ON gas_gasactivist USING btree (person_id);


--
-- Name: gas_gasconfig_default_delivery_place_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gasconfig_default_delivery_place_id ON gas_gasconfig USING btree (default_delivery_place_id);


--
-- Name: gas_gasconfig_default_withdrawal_place_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gasconfig_default_withdrawal_place_id ON gas_gasconfig USING btree (default_withdrawal_place_id);


--
-- Name: gas_gasconfig_default_workflow_gasmember_order_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gasconfig_default_workflow_gasmember_order_id ON gas_gasconfig USING btree (default_workflow_gasmember_order_id);


--
-- Name: gas_gasconfig_default_workflow_gassupplier_order_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gasconfig_default_workflow_gassupplier_order_id ON gas_gasconfig USING btree (default_workflow_gassupplier_order_id);


--
-- Name: gas_gasconfig_intergas_connection_set_gas_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gasconfig_intergas_connection_set_gas_id ON gas_gasconfig_intergas_connection_set USING btree (gas_id);


--
-- Name: gas_gasconfig_intergas_connection_set_gasconfig_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gasconfig_intergas_connection_set_gasconfig_id ON gas_gasconfig_intergas_connection_set USING btree (gasconfig_id);


--
-- Name: gas_gasconfig_is_suspended; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gasconfig_is_suspended ON gas_gasconfig USING btree (is_suspended);


--
-- Name: gas_gasconfig_suspend_auto_resume; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gasconfig_suspend_auto_resume ON gas_gasconfig USING btree (suspend_auto_resume);


--
-- Name: gas_gasmember_available_for_roles_gasmember_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gasmember_available_for_roles_gasmember_id ON gas_gasmember_available_for_roles USING btree (gasmember_id);


--
-- Name: gas_gasmember_available_for_roles_role_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gasmember_available_for_roles_role_id ON gas_gasmember_available_for_roles USING btree (role_id);


--
-- Name: gas_gasmember_gas_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gasmember_gas_id ON gas_gasmember USING btree (gas_id);


--
-- Name: gas_gasmember_is_suspended; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gasmember_is_suspended ON gas_gasmember USING btree (is_suspended);


--
-- Name: gas_gasmember_person_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gasmember_person_id ON gas_gasmember USING btree (person_id);


--
-- Name: gas_gasmember_suspend_auto_resume; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gasmember_suspend_auto_resume ON gas_gasmember USING btree (suspend_auto_resume);


--
-- Name: gas_gasmemberorder_ordered_product_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gasmemberorder_ordered_product_id ON gas_gasmemberorder USING btree (ordered_product_id);


--
-- Name: gas_gasmemberorder_purchaser_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gasmemberorder_purchaser_id ON gas_gasmemberorder USING btree (purchaser_id);


--
-- Name: gas_gassupplierorder_delivery_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gassupplierorder_delivery_id ON gas_gassupplierorder USING btree (delivery_id);


--
-- Name: gas_gassupplierorder_delivery_referrer_person_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gassupplierorder_delivery_referrer_person_id ON gas_gassupplierorder USING btree (delivery_referrer_person_id);


--
-- Name: gas_gassupplierorder_pact_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gassupplierorder_pact_id ON gas_gassupplierorder USING btree (pact_id);


--
-- Name: gas_gassupplierorder_referrer_person_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gassupplierorder_referrer_person_id ON gas_gassupplierorder USING btree (referrer_person_id);


--
-- Name: gas_gassupplierorder_root_plan_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gassupplierorder_root_plan_id ON gas_gassupplierorder USING btree (root_plan_id);


--
-- Name: gas_gassupplierorder_withdrawal_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gassupplierorder_withdrawal_id ON gas_gassupplierorder USING btree (withdrawal_id);


--
-- Name: gas_gassupplierorder_withdrawal_referrer_person_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gassupplierorder_withdrawal_referrer_person_id ON gas_gassupplierorder USING btree (withdrawal_referrer_person_id);


--
-- Name: gas_gassupplierorderproduct_gasstock_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gassupplierorderproduct_gasstock_id ON gas_gassupplierorderproduct USING btree (gasstock_id);


--
-- Name: gas_gassupplierorderproduct_order_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gassupplierorderproduct_order_id ON gas_gassupplierorderproduct USING btree (order_id);


--
-- Name: gas_gassuppliersolidalpact_default_delivery_place_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gassuppliersolidalpact_default_delivery_place_id ON gas_gassuppliersolidalpact USING btree (default_delivery_place_id);


--
-- Name: gas_gassuppliersolidalpact_gas_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gassuppliersolidalpact_gas_id ON gas_gassuppliersolidalpact USING btree (gas_id);


--
-- Name: gas_gassuppliersolidalpact_is_suspended; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gassuppliersolidalpact_is_suspended ON gas_gassuppliersolidalpact USING btree (is_suspended);


--
-- Name: gas_gassuppliersolidalpact_supplier_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gassuppliersolidalpact_supplier_id ON gas_gassuppliersolidalpact USING btree (supplier_id);


--
-- Name: gas_gassuppliersolidalpact_suspend_auto_resume; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gassuppliersolidalpact_suspend_auto_resume ON gas_gassuppliersolidalpact USING btree (suspend_auto_resume);


--
-- Name: gas_gassupplierstock_pact_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gassupplierstock_pact_id ON gas_gassupplierstock USING btree (pact_id);


--
-- Name: gas_gassupplierstock_stock_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_gassupplierstock_stock_id ON gas_gassupplierstock USING btree (stock_id);


--
-- Name: gas_historicaldelivery_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicaldelivery_history_user_id ON gas_historicaldelivery USING btree (history_user_id);


--
-- Name: gas_historicaldelivery_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicaldelivery_id ON gas_historicaldelivery USING btree (id);


--
-- Name: gas_historicaldelivery_place_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicaldelivery_place_id ON gas_historicaldelivery USING btree (place_id);


--
-- Name: gas_historicalgas_des_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgas_des_id ON gas_historicalgas USING btree (des_id);


--
-- Name: gas_historicalgas_headquarter_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgas_headquarter_id ON gas_historicalgas USING btree (headquarter_id);


--
-- Name: gas_historicalgas_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgas_history_user_id ON gas_historicalgas USING btree (history_user_id);


--
-- Name: gas_historicalgas_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgas_id ON gas_historicalgas USING btree (id);


--
-- Name: gas_historicalgas_id_in_des; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgas_id_in_des ON gas_historicalgas USING btree (id_in_des);


--
-- Name: gas_historicalgas_id_in_des_like; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgas_id_in_des_like ON gas_historicalgas USING btree (id_in_des varchar_pattern_ops);


--
-- Name: gas_historicalgas_name; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgas_name ON gas_historicalgas USING btree (name);


--
-- Name: gas_historicalgas_name_like; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgas_name_like ON gas_historicalgas USING btree (name varchar_pattern_ops);


--
-- Name: gas_historicalgas_orders_email_contact_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgas_orders_email_contact_id ON gas_historicalgas USING btree (orders_email_contact_id);


--
-- Name: gas_historicalgasactivist_gas_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasactivist_gas_id ON gas_historicalgasactivist USING btree (gas_id);


--
-- Name: gas_historicalgasactivist_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasactivist_history_user_id ON gas_historicalgasactivist USING btree (history_user_id);


--
-- Name: gas_historicalgasactivist_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasactivist_id ON gas_historicalgasactivist USING btree (id);


--
-- Name: gas_historicalgasactivist_person_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasactivist_person_id ON gas_historicalgasactivist USING btree (person_id);


--
-- Name: gas_historicalgasconfig_default_delivery_place_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasconfig_default_delivery_place_id ON gas_historicalgasconfig USING btree (default_delivery_place_id);


--
-- Name: gas_historicalgasconfig_default_withdrawal_place_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasconfig_default_withdrawal_place_id ON gas_historicalgasconfig USING btree (default_withdrawal_place_id);


--
-- Name: gas_historicalgasconfig_default_workflow_gasmember_order_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasconfig_default_workflow_gasmember_order_id ON gas_historicalgasconfig USING btree (default_workflow_gasmember_order_id);


--
-- Name: gas_historicalgasconfig_default_workflow_gassupplier_order_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasconfig_default_workflow_gassupplier_order_id ON gas_historicalgasconfig USING btree (default_workflow_gassupplier_order_id);


--
-- Name: gas_historicalgasconfig_gas_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasconfig_gas_id ON gas_historicalgasconfig USING btree (gas_id);


--
-- Name: gas_historicalgasconfig_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasconfig_history_user_id ON gas_historicalgasconfig USING btree (history_user_id);


--
-- Name: gas_historicalgasconfig_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasconfig_id ON gas_historicalgasconfig USING btree (id);


--
-- Name: gas_historicalgasconfig_is_suspended; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasconfig_is_suspended ON gas_historicalgasconfig USING btree (is_suspended);


--
-- Name: gas_historicalgasconfig_suspend_auto_resume; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasconfig_suspend_auto_resume ON gas_historicalgasconfig USING btree (suspend_auto_resume);


--
-- Name: gas_historicalgasmember_gas_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasmember_gas_id ON gas_historicalgasmember USING btree (gas_id);


--
-- Name: gas_historicalgasmember_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasmember_history_user_id ON gas_historicalgasmember USING btree (history_user_id);


--
-- Name: gas_historicalgasmember_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasmember_id ON gas_historicalgasmember USING btree (id);


--
-- Name: gas_historicalgasmember_is_suspended; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasmember_is_suspended ON gas_historicalgasmember USING btree (is_suspended);


--
-- Name: gas_historicalgasmember_person_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasmember_person_id ON gas_historicalgasmember USING btree (person_id);


--
-- Name: gas_historicalgasmember_suspend_auto_resume; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasmember_suspend_auto_resume ON gas_historicalgasmember USING btree (suspend_auto_resume);


--
-- Name: gas_historicalgasmemberorder_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasmemberorder_history_user_id ON gas_historicalgasmemberorder USING btree (history_user_id);


--
-- Name: gas_historicalgasmemberorder_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasmemberorder_id ON gas_historicalgasmemberorder USING btree (id);


--
-- Name: gas_historicalgasmemberorder_ordered_product_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasmemberorder_ordered_product_id ON gas_historicalgasmemberorder USING btree (ordered_product_id);


--
-- Name: gas_historicalgasmemberorder_purchaser_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgasmemberorder_purchaser_id ON gas_historicalgasmemberorder USING btree (purchaser_id);


--
-- Name: gas_historicalgassupplierorder_delivery_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassupplierorder_delivery_id ON gas_historicalgassupplierorder USING btree (delivery_id);


--
-- Name: gas_historicalgassupplierorder_delivery_referrer_person_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassupplierorder_delivery_referrer_person_id ON gas_historicalgassupplierorder USING btree (delivery_referrer_person_id);


--
-- Name: gas_historicalgassupplierorder_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassupplierorder_history_user_id ON gas_historicalgassupplierorder USING btree (history_user_id);


--
-- Name: gas_historicalgassupplierorder_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassupplierorder_id ON gas_historicalgassupplierorder USING btree (id);


--
-- Name: gas_historicalgassupplierorder_pact_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassupplierorder_pact_id ON gas_historicalgassupplierorder USING btree (pact_id);


--
-- Name: gas_historicalgassupplierorder_referrer_person_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassupplierorder_referrer_person_id ON gas_historicalgassupplierorder USING btree (referrer_person_id);


--
-- Name: gas_historicalgassupplierorder_root_plan_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassupplierorder_root_plan_id ON gas_historicalgassupplierorder USING btree (root_plan_id);


--
-- Name: gas_historicalgassupplierorder_withdrawal_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassupplierorder_withdrawal_id ON gas_historicalgassupplierorder USING btree (withdrawal_id);


--
-- Name: gas_historicalgassupplierorder_withdrawal_referrer_person_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassupplierorder_withdrawal_referrer_person_id ON gas_historicalgassupplierorder USING btree (withdrawal_referrer_person_id);


--
-- Name: gas_historicalgassupplierorderproduct_gasstock_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassupplierorderproduct_gasstock_id ON gas_historicalgassupplierorderproduct USING btree (gasstock_id);


--
-- Name: gas_historicalgassupplierorderproduct_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassupplierorderproduct_history_user_id ON gas_historicalgassupplierorderproduct USING btree (history_user_id);


--
-- Name: gas_historicalgassupplierorderproduct_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassupplierorderproduct_id ON gas_historicalgassupplierorderproduct USING btree (id);


--
-- Name: gas_historicalgassupplierorderproduct_order_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassupplierorderproduct_order_id ON gas_historicalgassupplierorderproduct USING btree (order_id);


--
-- Name: gas_historicalgassuppliersolidalpact_default_delivery_place_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassuppliersolidalpact_default_delivery_place_id ON gas_historicalgassuppliersolidalpact USING btree (default_delivery_place_id);


--
-- Name: gas_historicalgassuppliersolidalpact_gas_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassuppliersolidalpact_gas_id ON gas_historicalgassuppliersolidalpact USING btree (gas_id);


--
-- Name: gas_historicalgassuppliersolidalpact_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassuppliersolidalpact_history_user_id ON gas_historicalgassuppliersolidalpact USING btree (history_user_id);


--
-- Name: gas_historicalgassuppliersolidalpact_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassuppliersolidalpact_id ON gas_historicalgassuppliersolidalpact USING btree (id);


--
-- Name: gas_historicalgassuppliersolidalpact_is_suspended; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassuppliersolidalpact_is_suspended ON gas_historicalgassuppliersolidalpact USING btree (is_suspended);


--
-- Name: gas_historicalgassuppliersolidalpact_supplier_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassuppliersolidalpact_supplier_id ON gas_historicalgassuppliersolidalpact USING btree (supplier_id);


--
-- Name: gas_historicalgassuppliersolidalpact_suspend_auto_resume; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassuppliersolidalpact_suspend_auto_resume ON gas_historicalgassuppliersolidalpact USING btree (suspend_auto_resume);


--
-- Name: gas_historicalgassupplierstock_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassupplierstock_history_user_id ON gas_historicalgassupplierstock USING btree (history_user_id);


--
-- Name: gas_historicalgassupplierstock_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassupplierstock_id ON gas_historicalgassupplierstock USING btree (id);


--
-- Name: gas_historicalgassupplierstock_pact_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassupplierstock_pact_id ON gas_historicalgassupplierstock USING btree (pact_id);


--
-- Name: gas_historicalgassupplierstock_stock_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalgassupplierstock_stock_id ON gas_historicalgassupplierstock USING btree (stock_id);


--
-- Name: gas_historicalwithdrawal_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalwithdrawal_history_user_id ON gas_historicalwithdrawal USING btree (history_user_id);


--
-- Name: gas_historicalwithdrawal_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalwithdrawal_id ON gas_historicalwithdrawal USING btree (id);


--
-- Name: gas_historicalwithdrawal_place_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_historicalwithdrawal_place_id ON gas_historicalwithdrawal USING btree (place_id);


--
-- Name: gas_withdrawal_place_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX gas_withdrawal_place_id ON gas_withdrawal USING btree (place_id);


--
-- Name: notification_notice_notice_type_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX notification_notice_notice_type_id ON notification_notice USING btree (notice_type_id);


--
-- Name: notification_notice_recipient_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX notification_notice_recipient_id ON notification_notice USING btree (recipient_id);


--
-- Name: notification_notice_sender_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX notification_notice_sender_id ON notification_notice USING btree (sender_id);


--
-- Name: notification_noticesetting_notice_type_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX notification_noticesetting_notice_type_id ON notification_noticesetting USING btree (notice_type_id);


--
-- Name: notification_noticesetting_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX notification_noticesetting_user_id ON notification_noticesetting USING btree (user_id);


--
-- Name: notification_observeditem_content_type_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX notification_observeditem_content_type_id ON notification_observeditem USING btree (content_type_id);


--
-- Name: notification_observeditem_notice_type_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX notification_observeditem_notice_type_id ON notification_observeditem USING btree (notice_type_id);


--
-- Name: notification_observeditem_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX notification_observeditem_user_id ON notification_observeditem USING btree (user_id);


--
-- Name: permissions_objectpermission_content_type_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX permissions_objectpermission_content_type_id ON permissions_objectpermission USING btree (content_type_id);


--
-- Name: permissions_objectpermission_permission_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX permissions_objectpermission_permission_id ON permissions_objectpermission USING btree (permission_id);


--
-- Name: permissions_objectpermission_role_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX permissions_objectpermission_role_id ON permissions_objectpermission USING btree (role_id);


--
-- Name: permissions_objectpermissioninheritanceblock_content_type_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX permissions_objectpermissioninheritanceblock_content_type_id ON permissions_objectpermissioninheritanceblock USING btree (content_type_id);


--
-- Name: permissions_objectpermissioninheritanceblock_permission_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX permissions_objectpermissioninheritanceblock_permission_id ON permissions_objectpermissioninheritanceblock USING btree (permission_id);


--
-- Name: permissions_permission_content_types_contenttype_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX permissions_permission_content_types_contenttype_id ON permissions_permission_content_types USING btree (contenttype_id);


--
-- Name: permissions_permission_content_types_permission_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX permissions_permission_content_types_permission_id ON permissions_permission_content_types USING btree (permission_id);


--
-- Name: permissions_principalrolerelation_content_type_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX permissions_principalrolerelation_content_type_id ON permissions_principalrolerelation USING btree (content_type_id);


--
-- Name: permissions_principalrolerelation_group_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX permissions_principalrolerelation_group_id ON permissions_principalrolerelation USING btree (group_id);


--
-- Name: permissions_principalrolerelation_role_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX permissions_principalrolerelation_role_id ON permissions_principalrolerelation USING btree (role_id);


--
-- Name: permissions_principalrolerelation_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX permissions_principalrolerelation_user_id ON permissions_principalrolerelation USING btree (user_id);


--
-- Name: rest_homepage_resource_ctype_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX rest_homepage_resource_ctype_id ON rest_homepage USING btree (resource_ctype_id);


--
-- Name: rest_homepage_role_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX rest_homepage_role_id ON rest_homepage USING btree (role_id);


--
-- Name: rest_homepage_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX rest_homepage_user_id ON rest_homepage USING btree (user_id);


--
-- Name: rest_page_resource_ctype_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX rest_page_resource_ctype_id ON rest_page USING btree (resource_ctype_id);


--
-- Name: rest_page_role_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX rest_page_role_id ON rest_page USING btree (role_id);


--
-- Name: rest_page_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX rest_page_user_id ON rest_page USING btree (user_id);


--
-- Name: simple_accounting_account_kind_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX simple_accounting_account_kind_id ON simple_accounting_account USING btree (kind_id);


--
-- Name: simple_accounting_account_parent_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX simple_accounting_account_parent_id ON simple_accounting_account USING btree (parent_id);


--
-- Name: simple_accounting_account_system_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX simple_accounting_account_system_id ON simple_accounting_account USING btree (system_id);


--
-- Name: simple_accounting_cashflow_account_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX simple_accounting_cashflow_account_id ON simple_accounting_cashflow USING btree (account_id);


--
-- Name: simple_accounting_invoice_issuer_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX simple_accounting_invoice_issuer_id ON simple_accounting_invoice USING btree (issuer_id);


--
-- Name: simple_accounting_invoice_recipient_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX simple_accounting_invoice_recipient_id ON simple_accounting_invoice USING btree (recipient_id);


--
-- Name: simple_accounting_ledgerentry_account_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX simple_accounting_ledgerentry_account_id ON simple_accounting_ledgerentry USING btree (account_id);


--
-- Name: simple_accounting_ledgerentry_transaction_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX simple_accounting_ledgerentry_transaction_id ON simple_accounting_ledgerentry USING btree (transaction_id);


--
-- Name: simple_accounting_split_entry_point_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX simple_accounting_split_entry_point_id ON simple_accounting_split USING btree (entry_point_id);


--
-- Name: simple_accounting_split_exit_point_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX simple_accounting_split_exit_point_id ON simple_accounting_split USING btree (exit_point_id);


--
-- Name: simple_accounting_split_target_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX simple_accounting_split_target_id ON simple_accounting_split USING btree (target_id);


--
-- Name: simple_accounting_subject_content_type_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX simple_accounting_subject_content_type_id ON simple_accounting_subject USING btree (content_type_id);


--
-- Name: simple_accounting_transaction_issuer_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX simple_accounting_transaction_issuer_id ON simple_accounting_transaction USING btree (issuer_id);


--
-- Name: simple_accounting_transaction_source_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX simple_accounting_transaction_source_id ON simple_accounting_transaction USING btree (source_id);


--
-- Name: simple_accounting_transaction_split_set_split_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX simple_accounting_transaction_split_set_split_id ON simple_accounting_transaction_split_set USING btree (split_id);


--
-- Name: simple_accounting_transaction_split_set_transaction_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX simple_accounting_transaction_split_set_transaction_id ON simple_accounting_transaction_split_set USING btree (transaction_id);


--
-- Name: simple_accounting_transactionreference_content_type_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX simple_accounting_transactionreference_content_type_id ON simple_accounting_transactionreference USING btree (content_type_id);


--
-- Name: simple_accounting_transactionreference_transaction_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX simple_accounting_transactionreference_transaction_id ON simple_accounting_transactionreference USING btree (transaction_id);


--
-- Name: supplier_historicalcertification_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalcertification_history_user_id ON supplier_historicalcertification USING btree (history_user_id);


--
-- Name: supplier_historicalcertification_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalcertification_id ON supplier_historicalcertification USING btree (id);


--
-- Name: supplier_historicalcertification_name; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalcertification_name ON supplier_historicalcertification USING btree (name);


--
-- Name: supplier_historicalcertification_name_like; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalcertification_name_like ON supplier_historicalcertification USING btree (name varchar_pattern_ops);


--
-- Name: supplier_historicalcertification_symbol; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalcertification_symbol ON supplier_historicalcertification USING btree (symbol);


--
-- Name: supplier_historicalcertification_symbol_like; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalcertification_symbol_like ON supplier_historicalcertification USING btree (symbol varchar_pattern_ops);


--
-- Name: supplier_historicalproduct_category_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproduct_category_id ON supplier_historicalproduct USING btree (category_id);


--
-- Name: supplier_historicalproduct_code; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproduct_code ON supplier_historicalproduct USING btree (code);


--
-- Name: supplier_historicalproduct_code_like; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproduct_code_like ON supplier_historicalproduct USING btree (code varchar_pattern_ops);


--
-- Name: supplier_historicalproduct_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproduct_history_user_id ON supplier_historicalproduct USING btree (history_user_id);


--
-- Name: supplier_historicalproduct_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproduct_id ON supplier_historicalproduct USING btree (id);


--
-- Name: supplier_historicalproduct_mu_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproduct_mu_id ON supplier_historicalproduct USING btree (mu_id);


--
-- Name: supplier_historicalproduct_producer_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproduct_producer_id ON supplier_historicalproduct USING btree (producer_id);


--
-- Name: supplier_historicalproduct_pu_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproduct_pu_id ON supplier_historicalproduct USING btree (pu_id);


--
-- Name: supplier_historicalproductcategory_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproductcategory_history_user_id ON supplier_historicalproductcategory USING btree (history_user_id);


--
-- Name: supplier_historicalproductcategory_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproductcategory_id ON supplier_historicalproductcategory USING btree (id);


--
-- Name: supplier_historicalproductcategory_name; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproductcategory_name ON supplier_historicalproductcategory USING btree (name);


--
-- Name: supplier_historicalproductcategory_name_like; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproductcategory_name_like ON supplier_historicalproductcategory USING btree (name varchar_pattern_ops);


--
-- Name: supplier_historicalproductmu_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproductmu_history_user_id ON supplier_historicalproductmu USING btree (history_user_id);


--
-- Name: supplier_historicalproductmu_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproductmu_id ON supplier_historicalproductmu USING btree (id);


--
-- Name: supplier_historicalproductmu_name; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproductmu_name ON supplier_historicalproductmu USING btree (name);


--
-- Name: supplier_historicalproductmu_name_like; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproductmu_name_like ON supplier_historicalproductmu USING btree (name varchar_pattern_ops);


--
-- Name: supplier_historicalproductmu_symbol; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproductmu_symbol ON supplier_historicalproductmu USING btree (symbol);


--
-- Name: supplier_historicalproductmu_symbol_like; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproductmu_symbol_like ON supplier_historicalproductmu USING btree (symbol varchar_pattern_ops);


--
-- Name: supplier_historicalproductpu_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproductpu_history_user_id ON supplier_historicalproductpu USING btree (history_user_id);


--
-- Name: supplier_historicalproductpu_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproductpu_id ON supplier_historicalproductpu USING btree (id);


--
-- Name: supplier_historicalproductpu_name; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproductpu_name ON supplier_historicalproductpu USING btree (name);


--
-- Name: supplier_historicalproductpu_name_like; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproductpu_name_like ON supplier_historicalproductpu USING btree (name varchar_pattern_ops);


--
-- Name: supplier_historicalproductpu_symbol; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproductpu_symbol ON supplier_historicalproductpu USING btree (symbol);


--
-- Name: supplier_historicalproductpu_symbol_like; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalproductpu_symbol_like ON supplier_historicalproductpu USING btree (symbol varchar_pattern_ops);


--
-- Name: supplier_historicalsupplier_frontman_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalsupplier_frontman_id ON supplier_historicalsupplier USING btree (frontman_id);


--
-- Name: supplier_historicalsupplier_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalsupplier_history_user_id ON supplier_historicalsupplier USING btree (history_user_id);


--
-- Name: supplier_historicalsupplier_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalsupplier_id ON supplier_historicalsupplier USING btree (id);


--
-- Name: supplier_historicalsupplier_seat_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalsupplier_seat_id ON supplier_historicalsupplier USING btree (seat_id);


--
-- Name: supplier_historicalsupplier_ssn; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalsupplier_ssn ON supplier_historicalsupplier USING btree (ssn);


--
-- Name: supplier_historicalsupplier_ssn_like; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalsupplier_ssn_like ON supplier_historicalsupplier USING btree (ssn varchar_pattern_ops);


--
-- Name: supplier_historicalsupplier_vat_number; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalsupplier_vat_number ON supplier_historicalsupplier USING btree (vat_number);


--
-- Name: supplier_historicalsupplier_vat_number_like; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalsupplier_vat_number_like ON supplier_historicalsupplier USING btree (vat_number varchar_pattern_ops);


--
-- Name: supplier_historicalsupplieragent_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalsupplieragent_history_user_id ON supplier_historicalsupplieragent USING btree (history_user_id);


--
-- Name: supplier_historicalsupplieragent_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalsupplieragent_id ON supplier_historicalsupplieragent USING btree (id);


--
-- Name: supplier_historicalsupplieragent_person_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalsupplieragent_person_id ON supplier_historicalsupplieragent USING btree (person_id);


--
-- Name: supplier_historicalsupplieragent_supplier_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalsupplieragent_supplier_id ON supplier_historicalsupplieragent USING btree (supplier_id);


--
-- Name: supplier_historicalsupplierstock_history_user_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalsupplierstock_history_user_id ON supplier_historicalsupplierstock USING btree (history_user_id);


--
-- Name: supplier_historicalsupplierstock_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalsupplierstock_id ON supplier_historicalsupplierstock USING btree (id);


--
-- Name: supplier_historicalsupplierstock_product_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalsupplierstock_product_id ON supplier_historicalsupplierstock USING btree (product_id);


--
-- Name: supplier_historicalsupplierstock_supplier_category_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalsupplierstock_supplier_category_id ON supplier_historicalsupplierstock USING btree (supplier_category_id);


--
-- Name: supplier_historicalsupplierstock_supplier_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_historicalsupplierstock_supplier_id ON supplier_historicalsupplierstock USING btree (supplier_id);


--
-- Name: supplier_product_category_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_product_category_id ON supplier_product USING btree (category_id);


--
-- Name: supplier_product_mu_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_product_mu_id ON supplier_product USING btree (mu_id);


--
-- Name: supplier_product_producer_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_product_producer_id ON supplier_product USING btree (producer_id);


--
-- Name: supplier_product_pu_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_product_pu_id ON supplier_product USING btree (pu_id);


--
-- Name: supplier_supplier_certifications_certification_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_supplier_certifications_certification_id ON supplier_supplier_certifications USING btree (certification_id);


--
-- Name: supplier_supplier_certifications_supplier_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_supplier_certifications_supplier_id ON supplier_supplier_certifications USING btree (supplier_id);


--
-- Name: supplier_supplier_contact_set_contact_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_supplier_contact_set_contact_id ON supplier_supplier_contact_set USING btree (contact_id);


--
-- Name: supplier_supplier_contact_set_supplier_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_supplier_contact_set_supplier_id ON supplier_supplier_contact_set USING btree (supplier_id);


--
-- Name: supplier_supplier_frontman_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_supplier_frontman_id ON supplier_supplier USING btree (frontman_id);


--
-- Name: supplier_supplier_seat_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_supplier_seat_id ON supplier_supplier USING btree (seat_id);


--
-- Name: supplier_supplieragent_person_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_supplieragent_person_id ON supplier_supplieragent USING btree (person_id);


--
-- Name: supplier_supplieragent_supplier_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_supplieragent_supplier_id ON supplier_supplieragent USING btree (supplier_id);


--
-- Name: supplier_supplierconfig_products_made_by_set_supplier_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_supplierconfig_products_made_by_set_supplier_id ON supplier_supplierconfig_products_made_by_set USING btree (supplier_id);


--
-- Name: supplier_supplierconfig_products_made_by_set_supplierconfig_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_supplierconfig_products_made_by_set_supplierconfig_id ON supplier_supplierconfig_products_made_by_set USING btree (supplierconfig_id);


--
-- Name: supplier_supplierproductcategory_supplier_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_supplierproductcategory_supplier_id ON supplier_supplierproductcategory USING btree (supplier_id);


--
-- Name: supplier_supplierstock_product_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_supplierstock_product_id ON supplier_supplierstock USING btree (product_id);


--
-- Name: supplier_supplierstock_supplier_category_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_supplierstock_supplier_category_id ON supplier_supplierstock USING btree (supplier_category_id);


--
-- Name: supplier_supplierstock_supplier_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_supplierstock_supplier_id ON supplier_supplierstock USING btree (supplier_id);


--
-- Name: supplier_unitsconversion_dst_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_unitsconversion_dst_id ON supplier_unitsconversion USING btree (dst_id);


--
-- Name: supplier_unitsconversion_src_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX supplier_unitsconversion_src_id ON supplier_unitsconversion USING btree (src_id);


--
-- Name: users_userprofile_default_role_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX users_userprofile_default_role_id ON users_userprofile USING btree (default_role_id);


--
-- Name: workflows_state_transitions_state_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX workflows_state_transitions_state_id ON workflows_state_transitions USING btree (state_id);


--
-- Name: workflows_state_transitions_transition_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX workflows_state_transitions_transition_id ON workflows_state_transitions USING btree (transition_id);


--
-- Name: workflows_state_workflow_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX workflows_state_workflow_id ON workflows_state USING btree (workflow_id);


--
-- Name: workflows_stateinheritanceblock_permission_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX workflows_stateinheritanceblock_permission_id ON workflows_stateinheritanceblock USING btree (permission_id);


--
-- Name: workflows_stateinheritanceblock_state_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX workflows_stateinheritanceblock_state_id ON workflows_stateinheritanceblock USING btree (state_id);


--
-- Name: workflows_stateobjectrelation_content_type_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX workflows_stateobjectrelation_content_type_id ON workflows_stateobjectrelation USING btree (content_type_id);


--
-- Name: workflows_stateobjectrelation_state_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX workflows_stateobjectrelation_state_id ON workflows_stateobjectrelation USING btree (state_id);


--
-- Name: workflows_statepermissionrelation_permission_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX workflows_statepermissionrelation_permission_id ON workflows_statepermissionrelation USING btree (permission_id);


--
-- Name: workflows_statepermissionrelation_role_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX workflows_statepermissionrelation_role_id ON workflows_statepermissionrelation USING btree (role_id);


--
-- Name: workflows_statepermissionrelation_state_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX workflows_statepermissionrelation_state_id ON workflows_statepermissionrelation USING btree (state_id);


--
-- Name: workflows_transition_destination_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX workflows_transition_destination_id ON workflows_transition USING btree (destination_id);


--
-- Name: workflows_transition_permission_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX workflows_transition_permission_id ON workflows_transition USING btree (permission_id);


--
-- Name: workflows_transition_workflow_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX workflows_transition_workflow_id ON workflows_transition USING btree (workflow_id);


--
-- Name: workflows_workflow_initial_state_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX workflows_workflow_initial_state_id ON workflows_workflow USING btree (initial_state_id);


--
-- Name: workflows_workflowmodelrelation_workflow_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX workflows_workflowmodelrelation_workflow_id ON workflows_workflowmodelrelation USING btree (workflow_id);


--
-- Name: workflows_workflowobjectrelation_content_type_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX workflows_workflowobjectrelation_content_type_id ON workflows_workflowobjectrelation USING btree (content_type_id);


--
-- Name: workflows_workflowobjectrelation_workflow_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX workflows_workflowobjectrelation_workflow_id ON workflows_workflowobjectrelation USING btree (workflow_id);


--
-- Name: workflows_workflowpermissionrelation_permission_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX workflows_workflowpermissionrelation_permission_id ON workflows_workflowpermissionrelation USING btree (permission_id);


--
-- Name: workflows_workflowpermissionrelation_workflow_id; Type: INDEX; Schema: public; Owner: gf_stage; Tablespace: 
--

CREATE INDEX workflows_workflowpermissionrelation_workflow_id ON workflows_workflowpermissionrelation USING btree (workflow_id);


--
-- Name: address_id_refs_id_41ed0496; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_person
    ADD CONSTRAINT address_id_refs_id_41ed0496 FOREIGN KEY (address_id) REFERENCES base_place(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: address_id_refs_id_6f4c4ef0; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_historicalperson
    ADD CONSTRAINT address_id_refs_id_6f4c4ef0 FOREIGN KEY (address_id) REFERENCES base_place(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_message_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_defaulttransition_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_defaulttransition
    ADD CONSTRAINT base_defaulttransition_state_id_fkey FOREIGN KEY (state_id) REFERENCES workflows_state(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_defaulttransition_transition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_defaulttransition
    ADD CONSTRAINT base_defaulttransition_transition_id_fkey FOREIGN KEY (transition_id) REFERENCES workflows_transition(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_defaulttransition_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_defaulttransition
    ADD CONSTRAINT base_defaulttransition_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES workflows_workflow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_historicaldefaulttransition_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_historicaldefaulttransition
    ADD CONSTRAINT base_historicaldefaulttransition_state_id_fkey FOREIGN KEY (state_id) REFERENCES workflows_state(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_historicaldefaulttransition_transition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_historicaldefaulttransition
    ADD CONSTRAINT base_historicaldefaulttransition_transition_id_fkey FOREIGN KEY (transition_id) REFERENCES workflows_transition(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_historicaldefaulttransition_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_historicaldefaulttransition
    ADD CONSTRAINT base_historicaldefaulttransition_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES workflows_workflow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: certification_id_refs_id_6fe4009f; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplier_certifications
    ADD CONSTRAINT certification_id_refs_id_6fe4009f FOREIGN KEY (certification_id) REFERENCES supplier_certification(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contact_id_refs_id_1f6a1969; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gas_contact_set
    ADD CONSTRAINT contact_id_refs_id_1f6a1969 FOREIGN KEY (contact_id) REFERENCES base_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contact_id_refs_id_aff6d47; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_person_contact_set
    ADD CONSTRAINT contact_id_refs_id_aff6d47 FOREIGN KEY (contact_id) REFERENCES base_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_1f26acd4; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_stateobjectrelation
    ADD CONSTRAINT content_type_id_refs_id_1f26acd4 FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_30b770a6; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY permissions_principalrolerelation
    ADD CONSTRAINT content_type_id_refs_id_30b770a6 FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_318265f7; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY flexi_auth_param
    ADD CONSTRAINT content_type_id_refs_id_318265f7 FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_37ca7887; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_workflowobjectrelation
    ADD CONSTRAINT content_type_id_refs_id_37ca7887 FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_40af626e; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_subject
    ADD CONSTRAINT content_type_id_refs_id_40af626e FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_43ab7380; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY permissions_objectpermissioninheritanceblock
    ADD CONSTRAINT content_type_id_refs_id_43ab7380 FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_489cfcfb; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY permissions_objectpermission
    ADD CONSTRAINT content_type_id_refs_id_489cfcfb FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_5cb41c92; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_workflowmodelrelation
    ADD CONSTRAINT content_type_id_refs_id_5cb41c92 FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_6b8c49bc; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_transactionreference
    ADD CONSTRAINT content_type_id_refs_id_6b8c49bc FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_728de91f; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT content_type_id_refs_id_728de91f FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contenttype_id_refs_id_7463a632; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY permissions_permission_content_types
    ADD CONSTRAINT contenttype_id_refs_id_7463a632 FOREIGN KEY (contenttype_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: default_delivery_place_id_refs_id_1d4daae1; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gassuppliersolidalpact
    ADD CONSTRAINT default_delivery_place_id_refs_id_1d4daae1 FOREIGN KEY (default_delivery_place_id) REFERENCES base_place(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: default_delivery_place_id_refs_id_373796b2; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasconfig
    ADD CONSTRAINT default_delivery_place_id_refs_id_373796b2 FOREIGN KEY (default_delivery_place_id) REFERENCES base_place(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: default_role_id_refs_id_168b262c; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY users_userprofile
    ADD CONSTRAINT default_role_id_refs_id_168b262c FOREIGN KEY (default_role_id) REFERENCES flexi_auth_paramrole(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: default_withdrawal_place_id_refs_id_373796b2; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasconfig
    ADD CONSTRAINT default_withdrawal_place_id_refs_id_373796b2 FOREIGN KEY (default_withdrawal_place_id) REFERENCES base_place(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: default_workflow_gasmember_order_id_refs_id_bbd4d91; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasconfig
    ADD CONSTRAINT default_workflow_gasmember_order_id_refs_id_bbd4d91 FOREIGN KEY (default_workflow_gasmember_order_id) REFERENCES workflows_workflow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: default_workflow_gassupplier_order_id_refs_id_bbd4d91; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasconfig
    ADD CONSTRAINT default_workflow_gassupplier_order_id_refs_id_bbd4d91 FOREIGN KEY (default_workflow_gassupplier_order_id) REFERENCES workflows_workflow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: delivery_id_refs_id_170e385e; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gassupplierorder
    ADD CONSTRAINT delivery_id_refs_id_170e385e FOREIGN KEY (delivery_id) REFERENCES gas_delivery(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: delivery_referrer_person_id_refs_id_6bcc7a2a; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gassupplierorder
    ADD CONSTRAINT delivery_referrer_person_id_refs_id_6bcc7a2a FOREIGN KEY (delivery_referrer_person_id) REFERENCES base_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: des_des_info_people_set_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY des_des_info_people_set
    ADD CONSTRAINT des_des_info_people_set_person_id_fkey FOREIGN KEY (person_id) REFERENCES base_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: des_des_site_ptr_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY des_des
    ADD CONSTRAINT des_des_site_ptr_id_fkey FOREIGN KEY (site_ptr_id) REFERENCES django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: des_id_refs_site_ptr_id_33f52a5d; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY des_des_info_people_set
    ADD CONSTRAINT des_id_refs_site_ptr_id_33f52a5d FOREIGN KEY (des_id) REFERENCES des_des(site_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: des_id_refs_site_ptr_id_53e97f6d; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gas
    ADD CONSTRAINT des_id_refs_site_ptr_id_53e97f6d FOREIGN KEY (des_id) REFERENCES des_des(site_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_content_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_comment_flags_comment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY django_comment_flags
    ADD CONSTRAINT django_comment_flags_comment_id_fkey FOREIGN KEY (comment_id) REFERENCES django_comments(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_comment_flags_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY django_comment_flags
    ADD CONSTRAINT django_comment_flags_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_comments_content_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY django_comments
    ADD CONSTRAINT django_comments_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_comments_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY django_comments
    ADD CONSTRAINT django_comments_site_id_fkey FOREIGN KEY (site_id) REFERENCES django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_comments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY django_comments
    ADD CONSTRAINT django_comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: flexi_auth_paramrole_param_set_param_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY flexi_auth_paramrole_param_set
    ADD CONSTRAINT flexi_auth_paramrole_param_set_param_id_fkey FOREIGN KEY (param_id) REFERENCES flexi_auth_param(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: flexi_auth_paramrole_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY flexi_auth_paramrole
    ADD CONSTRAINT flexi_auth_paramrole_role_id_fkey FOREIGN KEY (role_id) REFERENCES permissions_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: flexi_auth_principalparamrolerelation_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY flexi_auth_principalparamrolerelation
    ADD CONSTRAINT flexi_auth_principalparamrolerelation_role_id_fkey FOREIGN KEY (role_id) REFERENCES flexi_auth_paramrole(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gas_id_refs_id_18cb3598; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasactivist
    ADD CONSTRAINT gas_id_refs_id_18cb3598 FOREIGN KEY (gas_id) REFERENCES gas_gas(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gas_id_refs_id_25e51823; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasconfig_intergas_connection_set
    ADD CONSTRAINT gas_id_refs_id_25e51823 FOREIGN KEY (gas_id) REFERENCES gas_gas(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gas_id_refs_id_2ed2aac7; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasconfig
    ADD CONSTRAINT gas_id_refs_id_2ed2aac7 FOREIGN KEY (gas_id) REFERENCES gas_gas(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gas_id_refs_id_5f2b9947; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasmember
    ADD CONSTRAINT gas_id_refs_id_5f2b9947 FOREIGN KEY (gas_id) REFERENCES gas_gas(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gas_id_refs_id_7742ecc3; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gas_contact_set
    ADD CONSTRAINT gas_id_refs_id_7742ecc3 FOREIGN KEY (gas_id) REFERENCES gas_gas(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gas_id_refs_id_7ce06c5a; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gassuppliersolidalpact
    ADD CONSTRAINT gas_id_refs_id_7ce06c5a FOREIGN KEY (gas_id) REFERENCES gas_gas(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gasconfig_id_refs_id_6e9bda4d; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasconfig_intergas_connection_set
    ADD CONSTRAINT gasconfig_id_refs_id_6e9bda4d FOREIGN KEY (gasconfig_id) REFERENCES gas_gasconfig(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gasmember_id_refs_id_32397a4f; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasmember_available_for_roles
    ADD CONSTRAINT gasmember_id_refs_id_32397a4f FOREIGN KEY (gasmember_id) REFERENCES gas_gasmember(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gasstock_id_refs_id_6ef0e831; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gassupplierorderproduct
    ADD CONSTRAINT gasstock_id_refs_id_6ef0e831 FOREIGN KEY (gasstock_id) REFERENCES gas_gassupplierstock(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: group_id_refs_id_2998acd3; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY flexi_auth_principalparamrolerelation
    ADD CONSTRAINT group_id_refs_id_2998acd3 FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: group_id_refs_id_2cf79349; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY permissions_principalrolerelation
    ADD CONSTRAINT group_id_refs_id_2cf79349 FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: group_id_refs_id_3cea63fe; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT group_id_refs_id_3cea63fe FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: headquarter_id_refs_id_7d4a259e; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gas
    ADD CONSTRAINT headquarter_id_refs_id_7d4a259e FOREIGN KEY (headquarter_id) REFERENCES base_place(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_10040ba8; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_historicalperson
    ADD CONSTRAINT history_user_id_refs_id_10040ba8 FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_1257943f; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicalwithdrawal
    ADD CONSTRAINT history_user_id_refs_id_1257943f FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_17d046ff; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicalgassupplierorder
    ADD CONSTRAINT history_user_id_refs_id_17d046ff FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_1ae9b038; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicalgas
    ADD CONSTRAINT history_user_id_refs_id_1ae9b038 FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_1e80a262; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalproduct
    ADD CONSTRAINT history_user_id_refs_id_1e80a262 FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_1f3b75f8; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicaldelivery
    ADD CONSTRAINT history_user_id_refs_id_1f3b75f8 FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_254823cc; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicalgasmember
    ADD CONSTRAINT history_user_id_refs_id_254823cc FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_340532ee; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalproductcategory
    ADD CONSTRAINT history_user_id_refs_id_340532ee FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_3d68d30a; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalproductmu
    ADD CONSTRAINT history_user_id_refs_id_3d68d30a FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_3e65e6fb; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalcertification
    ADD CONSTRAINT history_user_id_refs_id_3e65e6fb FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_4008ab45; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_historicalplace
    ADD CONSTRAINT history_user_id_refs_id_4008ab45 FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_40f5382d; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicalgasactivist
    ADD CONSTRAINT history_user_id_refs_id_40f5382d FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_43fde4b7; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicalgassupplierstock
    ADD CONSTRAINT history_user_id_refs_id_43fde4b7 FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_4612457c; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicalgasconfig
    ADD CONSTRAINT history_user_id_refs_id_4612457c FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_4bee4edc; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalsupplier
    ADD CONSTRAINT history_user_id_refs_id_4bee4edc FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_55f1c17; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicalgassuppliersolidalpact
    ADD CONSTRAINT history_user_id_refs_id_55f1c17 FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_627812a0; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_historicalcontact
    ADD CONSTRAINT history_user_id_refs_id_627812a0 FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_6288cdc7; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalsupplierstock
    ADD CONSTRAINT history_user_id_refs_id_6288cdc7 FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_62cc8de8; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_historicaldefaulttransition
    ADD CONSTRAINT history_user_id_refs_id_62cc8de8 FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_69a32899; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicalgasmemberorder
    ADD CONSTRAINT history_user_id_refs_id_69a32899 FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_7ddfa6ad; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalproductpu
    ADD CONSTRAINT history_user_id_refs_id_7ddfa6ad FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_7fa172af; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_historicalgassupplierorderproduct
    ADD CONSTRAINT history_user_id_refs_id_7fa172af FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: history_user_id_refs_id_d9ae66e; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalsupplieragent
    ADD CONSTRAINT history_user_id_refs_id_d9ae66e FOREIGN KEY (history_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: initial_state_id_refs_id_6181b516; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_workflow
    ADD CONSTRAINT initial_state_id_refs_id_6181b516 FOREIGN KEY (initial_state_id) REFERENCES workflows_state(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notification_notice_notice_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY notification_notice
    ADD CONSTRAINT notification_notice_notice_type_id_fkey FOREIGN KEY (notice_type_id) REFERENCES notification_noticetype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notification_notice_recipient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY notification_notice
    ADD CONSTRAINT notification_notice_recipient_id_fkey FOREIGN KEY (recipient_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notification_notice_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY notification_notice
    ADD CONSTRAINT notification_notice_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notification_noticesetting_notice_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY notification_noticesetting
    ADD CONSTRAINT notification_noticesetting_notice_type_id_fkey FOREIGN KEY (notice_type_id) REFERENCES notification_noticetype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notification_noticesetting_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY notification_noticesetting
    ADD CONSTRAINT notification_noticesetting_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notification_observeditem_content_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY notification_observeditem
    ADD CONSTRAINT notification_observeditem_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notification_observeditem_notice_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY notification_observeditem
    ADD CONSTRAINT notification_observeditem_notice_type_id_fkey FOREIGN KEY (notice_type_id) REFERENCES notification_noticetype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: notification_observeditem_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY notification_observeditem
    ADD CONSTRAINT notification_observeditem_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: order_id_refs_id_68681509; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gassupplierorderproduct
    ADD CONSTRAINT order_id_refs_id_68681509 FOREIGN KEY (order_id) REFERENCES gas_gassupplierorder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ordered_product_id_refs_id_169143c5; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasmemberorder
    ADD CONSTRAINT ordered_product_id_refs_id_169143c5 FOREIGN KEY (ordered_product_id) REFERENCES gas_gassupplierorderproduct(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orders_email_contact_id_refs_id_26032963; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gas
    ADD CONSTRAINT orders_email_contact_id_refs_id_26032963 FOREIGN KEY (orders_email_contact_id) REFERENCES base_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pact_id_refs_id_286e7f6f; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gassupplierorder
    ADD CONSTRAINT pact_id_refs_id_286e7f6f FOREIGN KEY (pact_id) REFERENCES gas_gassuppliersolidalpact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: pact_id_refs_id_552c635f; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gassupplierstock
    ADD CONSTRAINT pact_id_refs_id_552c635f FOREIGN KEY (pact_id) REFERENCES gas_gassuppliersolidalpact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: paramrole_id_refs_id_278bb650; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY flexi_auth_paramrole_param_set
    ADD CONSTRAINT paramrole_id_refs_id_278bb650 FOREIGN KEY (paramrole_id) REFERENCES flexi_auth_paramrole(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: parent_id_refs_id_3c9a89e5; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_account
    ADD CONSTRAINT parent_id_refs_id_3c9a89e5 FOREIGN KEY (parent_id) REFERENCES simple_accounting_account(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: permission_id_refs_id_128eff21; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY permissions_permission_content_types
    ADD CONSTRAINT permission_id_refs_id_128eff21 FOREIGN KEY (permission_id) REFERENCES permissions_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: permissions_objectpermission_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY permissions_objectpermission
    ADD CONSTRAINT permissions_objectpermission_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES permissions_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: permissions_objectpermissioninheritanceblock_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY permissions_objectpermissioninheritanceblock
    ADD CONSTRAINT permissions_objectpermissioninheritanceblock_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES permissions_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: permissions_principalrolerelation_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY permissions_principalrolerelation
    ADD CONSTRAINT permissions_principalrolerelation_role_id_fkey FOREIGN KEY (role_id) REFERENCES permissions_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: person_id_refs_id_63c66360; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasactivist
    ADD CONSTRAINT person_id_refs_id_63c66360 FOREIGN KEY (person_id) REFERENCES base_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: person_id_refs_id_700fe96f; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasmember
    ADD CONSTRAINT person_id_refs_id_700fe96f FOREIGN KEY (person_id) REFERENCES base_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: person_id_refs_id_7772559b; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_person_contact_set
    ADD CONSTRAINT person_id_refs_id_7772559b FOREIGN KEY (person_id) REFERENCES base_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: place_id_refs_id_5f3ab247; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_withdrawal
    ADD CONSTRAINT place_id_refs_id_5f3ab247 FOREIGN KEY (place_id) REFERENCES base_place(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: place_id_refs_id_72e02f12; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_delivery
    ADD CONSTRAINT place_id_refs_id_72e02f12 FOREIGN KEY (place_id) REFERENCES base_place(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: purchaser_id_refs_id_2f5fd03e; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasmemberorder
    ADD CONSTRAINT purchaser_id_refs_id_2f5fd03e FOREIGN KEY (purchaser_id) REFERENCES gas_gasmember(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: referrer_person_id_refs_id_6bcc7a2a; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gassupplierorder
    ADD CONSTRAINT referrer_person_id_refs_id_6bcc7a2a FOREIGN KEY (referrer_person_id) REFERENCES base_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registration_registrationprofile_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY registration_registrationprofile
    ADD CONSTRAINT registration_registrationprofile_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: resource_ctype_id_refs_id_602910e8; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY rest_homepage
    ADD CONSTRAINT resource_ctype_id_refs_id_602910e8 FOREIGN KEY (resource_ctype_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: resource_ctype_id_refs_id_694dcf1; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY rest_page
    ADD CONSTRAINT resource_ctype_id_refs_id_694dcf1 FOREIGN KEY (resource_ctype_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rest_homepage_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY rest_homepage
    ADD CONSTRAINT rest_homepage_role_id_fkey FOREIGN KEY (role_id) REFERENCES flexi_auth_paramrole(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: rest_page_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY rest_page
    ADD CONSTRAINT rest_page_role_id_fkey FOREIGN KEY (role_id) REFERENCES flexi_auth_paramrole(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: role_id_refs_id_1268c29a; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gasmember_available_for_roles
    ADD CONSTRAINT role_id_refs_id_1268c29a FOREIGN KEY (role_id) REFERENCES permissions_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: role_id_refs_id_3b08a8db; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY permissions_objectpermission
    ADD CONSTRAINT role_id_refs_id_3b08a8db FOREIGN KEY (role_id) REFERENCES permissions_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: root_plan_id_refs_id_5afaa85; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gassupplierorder
    ADD CONSTRAINT root_plan_id_refs_id_5afaa85 FOREIGN KEY (root_plan_id) REFERENCES gas_gassupplierorder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: simple_accounting_account_kind_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_account
    ADD CONSTRAINT simple_accounting_account_kind_id_fkey FOREIGN KEY (kind_id) REFERENCES simple_accounting_accounttype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: simple_accounting_account_system_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_account
    ADD CONSTRAINT simple_accounting_account_system_id_fkey FOREIGN KEY (system_id) REFERENCES simple_accounting_accountsystem(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: simple_accounting_accountsystem_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_accountsystem
    ADD CONSTRAINT simple_accounting_accountsystem_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES simple_accounting_subject(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: simple_accounting_cashflow_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_cashflow
    ADD CONSTRAINT simple_accounting_cashflow_account_id_fkey FOREIGN KEY (account_id) REFERENCES simple_accounting_account(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: simple_accounting_invoice_issuer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_invoice
    ADD CONSTRAINT simple_accounting_invoice_issuer_id_fkey FOREIGN KEY (issuer_id) REFERENCES simple_accounting_subject(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: simple_accounting_invoice_recipient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_invoice
    ADD CONSTRAINT simple_accounting_invoice_recipient_id_fkey FOREIGN KEY (recipient_id) REFERENCES simple_accounting_subject(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: simple_accounting_ledgerentry_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_ledgerentry
    ADD CONSTRAINT simple_accounting_ledgerentry_account_id_fkey FOREIGN KEY (account_id) REFERENCES simple_accounting_account(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: simple_accounting_ledgerentry_transaction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_ledgerentry
    ADD CONSTRAINT simple_accounting_ledgerentry_transaction_id_fkey FOREIGN KEY (transaction_id) REFERENCES simple_accounting_transaction(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: simple_accounting_split_entry_point_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_split
    ADD CONSTRAINT simple_accounting_split_entry_point_id_fkey FOREIGN KEY (entry_point_id) REFERENCES simple_accounting_account(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: simple_accounting_split_exit_point_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_split
    ADD CONSTRAINT simple_accounting_split_exit_point_id_fkey FOREIGN KEY (exit_point_id) REFERENCES simple_accounting_account(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: simple_accounting_split_target_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_split
    ADD CONSTRAINT simple_accounting_split_target_id_fkey FOREIGN KEY (target_id) REFERENCES simple_accounting_cashflow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: simple_accounting_transaction_issuer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_transaction
    ADD CONSTRAINT simple_accounting_transaction_issuer_id_fkey FOREIGN KEY (issuer_id) REFERENCES simple_accounting_subject(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: simple_accounting_transaction_source_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_transaction
    ADD CONSTRAINT simple_accounting_transaction_source_id_fkey FOREIGN KEY (source_id) REFERENCES simple_accounting_cashflow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: simple_accounting_transaction_split_set_split_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_transaction_split_set
    ADD CONSTRAINT simple_accounting_transaction_split_set_split_id_fkey FOREIGN KEY (split_id) REFERENCES simple_accounting_split(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: simple_accounting_transactionreference_transaction_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_transactionreference
    ADD CONSTRAINT simple_accounting_transactionreference_transaction_id_fkey FOREIGN KEY (transaction_id) REFERENCES simple_accounting_transaction(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: state_id_refs_id_79136638; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_state_transitions
    ADD CONSTRAINT state_id_refs_id_79136638 FOREIGN KEY (state_id) REFERENCES workflows_state(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: stock_id_refs_id_10b27fdf; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gassupplierstock
    ADD CONSTRAINT stock_id_refs_id_10b27fdf FOREIGN KEY (stock_id) REFERENCES supplier_supplierstock(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_category_id_refs_id_369cd51c; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalsupplierstock
    ADD CONSTRAINT supplier_category_id_refs_id_369cd51c FOREIGN KEY (supplier_category_id) REFERENCES supplier_supplierproductcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_category_id_refs_id_77efe212; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplierstock
    ADD CONSTRAINT supplier_category_id_refs_id_77efe212 FOREIGN KEY (supplier_category_id) REFERENCES supplier_supplierproductcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_historicalproduct_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalproduct
    ADD CONSTRAINT supplier_historicalproduct_category_id_fkey FOREIGN KEY (category_id) REFERENCES supplier_productcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_historicalproduct_mu_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalproduct
    ADD CONSTRAINT supplier_historicalproduct_mu_id_fkey FOREIGN KEY (mu_id) REFERENCES supplier_productmu(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_historicalproduct_producer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalproduct
    ADD CONSTRAINT supplier_historicalproduct_producer_id_fkey FOREIGN KEY (producer_id) REFERENCES supplier_supplier(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_historicalproduct_pu_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalproduct
    ADD CONSTRAINT supplier_historicalproduct_pu_id_fkey FOREIGN KEY (pu_id) REFERENCES supplier_productpu(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_historicalsupplier_frontman_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalsupplier
    ADD CONSTRAINT supplier_historicalsupplier_frontman_id_fkey FOREIGN KEY (frontman_id) REFERENCES base_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_historicalsupplier_seat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalsupplier
    ADD CONSTRAINT supplier_historicalsupplier_seat_id_fkey FOREIGN KEY (seat_id) REFERENCES base_place(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_historicalsupplieragent_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalsupplieragent
    ADD CONSTRAINT supplier_historicalsupplieragent_person_id_fkey FOREIGN KEY (person_id) REFERENCES base_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_historicalsupplieragent_supplier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalsupplieragent
    ADD CONSTRAINT supplier_historicalsupplieragent_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES supplier_supplier(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_historicalsupplierstock_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalsupplierstock
    ADD CONSTRAINT supplier_historicalsupplierstock_product_id_fkey FOREIGN KEY (product_id) REFERENCES supplier_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_historicalsupplierstock_supplier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_historicalsupplierstock
    ADD CONSTRAINT supplier_historicalsupplierstock_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES supplier_supplier(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_id_refs_id_33242622; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplier_certifications
    ADD CONSTRAINT supplier_id_refs_id_33242622 FOREIGN KEY (supplier_id) REFERENCES supplier_supplier(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_id_refs_id_5a9a2a81; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplier_contact_set
    ADD CONSTRAINT supplier_id_refs_id_5a9a2a81 FOREIGN KEY (supplier_id) REFERENCES supplier_supplier(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_id_refs_id_e9968ee; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gassuppliersolidalpact
    ADD CONSTRAINT supplier_id_refs_id_e9968ee FOREIGN KEY (supplier_id) REFERENCES supplier_supplier(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_product_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_product
    ADD CONSTRAINT supplier_product_category_id_fkey FOREIGN KEY (category_id) REFERENCES supplier_productcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_product_mu_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_product
    ADD CONSTRAINT supplier_product_mu_id_fkey FOREIGN KEY (mu_id) REFERENCES supplier_productmu(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_product_producer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_product
    ADD CONSTRAINT supplier_product_producer_id_fkey FOREIGN KEY (producer_id) REFERENCES supplier_supplier(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_product_pu_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_product
    ADD CONSTRAINT supplier_product_pu_id_fkey FOREIGN KEY (pu_id) REFERENCES supplier_productpu(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_supplier_contact_set_contact_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplier_contact_set
    ADD CONSTRAINT supplier_supplier_contact_set_contact_id_fkey FOREIGN KEY (contact_id) REFERENCES base_contact(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_supplier_frontman_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplier
    ADD CONSTRAINT supplier_supplier_frontman_id_fkey FOREIGN KEY (frontman_id) REFERENCES base_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_supplier_seat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplier
    ADD CONSTRAINT supplier_supplier_seat_id_fkey FOREIGN KEY (seat_id) REFERENCES base_place(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_supplieragent_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplieragent
    ADD CONSTRAINT supplier_supplieragent_person_id_fkey FOREIGN KEY (person_id) REFERENCES base_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_supplieragent_supplier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplieragent
    ADD CONSTRAINT supplier_supplieragent_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES supplier_supplier(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_supplierconfig_products_made_by_set_supplier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplierconfig_products_made_by_set
    ADD CONSTRAINT supplier_supplierconfig_products_made_by_set_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES supplier_supplier(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_supplierconfig_supplier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplierconfig
    ADD CONSTRAINT supplier_supplierconfig_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES supplier_supplier(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_supplierproductcategory_supplier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplierproductcategory
    ADD CONSTRAINT supplier_supplierproductcategory_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES supplier_supplier(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_supplierstock_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplierstock
    ADD CONSTRAINT supplier_supplierstock_product_id_fkey FOREIGN KEY (product_id) REFERENCES supplier_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_supplierstock_supplier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplierstock
    ADD CONSTRAINT supplier_supplierstock_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES supplier_supplier(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_unitsconversion_dst_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_unitsconversion
    ADD CONSTRAINT supplier_unitsconversion_dst_id_fkey FOREIGN KEY (dst_id) REFERENCES supplier_productmu(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplier_unitsconversion_src_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_unitsconversion
    ADD CONSTRAINT supplier_unitsconversion_src_id_fkey FOREIGN KEY (src_id) REFERENCES supplier_productmu(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: supplierconfig_id_refs_id_e016ebc; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY supplier_supplierconfig_products_made_by_set
    ADD CONSTRAINT supplierconfig_id_refs_id_e016ebc FOREIGN KEY (supplierconfig_id) REFERENCES supplier_supplierconfig(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: transaction_id_refs_id_39d19361; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY simple_accounting_transaction_split_set
    ADD CONSTRAINT transaction_id_refs_id_39d19361 FOREIGN KEY (transaction_id) REFERENCES simple_accounting_transaction(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: transition_id_refs_id_5ee9988d; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_state_transitions
    ADD CONSTRAINT transition_id_refs_id_5ee9988d FOREIGN KEY (transition_id) REFERENCES workflows_transition(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_10040ba8; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_historicalperson
    ADD CONSTRAINT user_id_refs_id_10040ba8 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_1bfa267; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY blockconfiguration
    ADD CONSTRAINT user_id_refs_id_1bfa267 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_29ac45dc; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY users_userprofile
    ADD CONSTRAINT user_id_refs_id_29ac45dc FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_41b25c1a; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY flexi_auth_principalparamrolerelation
    ADD CONSTRAINT user_id_refs_id_41b25c1a FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_60a103ca; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY permissions_principalrolerelation
    ADD CONSTRAINT user_id_refs_id_60a103ca FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_667bd8fe; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY base_person
    ADD CONSTRAINT user_id_refs_id_667bd8fe FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_74891d6c; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY rest_homepage
    ADD CONSTRAINT user_id_refs_id_74891d6c FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_7ceef80f; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT user_id_refs_id_7ceef80f FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_dfbab7d; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT user_id_refs_id_dfbab7d FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_e9a6e45; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY rest_page
    ADD CONSTRAINT user_id_refs_id_e9a6e45 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: withdrawal_id_refs_id_6f8dae7f; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gassupplierorder
    ADD CONSTRAINT withdrawal_id_refs_id_6f8dae7f FOREIGN KEY (withdrawal_id) REFERENCES gas_withdrawal(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: withdrawal_referrer_person_id_refs_id_6bcc7a2a; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY gas_gassupplierorder
    ADD CONSTRAINT withdrawal_referrer_person_id_refs_id_6bcc7a2a FOREIGN KEY (withdrawal_referrer_person_id) REFERENCES base_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: workflows_state_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_state
    ADD CONSTRAINT workflows_state_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES workflows_workflow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: workflows_stateinheritanceblock_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_stateinheritanceblock
    ADD CONSTRAINT workflows_stateinheritanceblock_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES permissions_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: workflows_stateinheritanceblock_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_stateinheritanceblock
    ADD CONSTRAINT workflows_stateinheritanceblock_state_id_fkey FOREIGN KEY (state_id) REFERENCES workflows_state(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: workflows_stateobjectrelation_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_stateobjectrelation
    ADD CONSTRAINT workflows_stateobjectrelation_state_id_fkey FOREIGN KEY (state_id) REFERENCES workflows_state(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: workflows_statepermissionrelation_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_statepermissionrelation
    ADD CONSTRAINT workflows_statepermissionrelation_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES permissions_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: workflows_statepermissionrelation_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_statepermissionrelation
    ADD CONSTRAINT workflows_statepermissionrelation_role_id_fkey FOREIGN KEY (role_id) REFERENCES permissions_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: workflows_statepermissionrelation_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_statepermissionrelation
    ADD CONSTRAINT workflows_statepermissionrelation_state_id_fkey FOREIGN KEY (state_id) REFERENCES workflows_state(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: workflows_transition_destination_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_transition
    ADD CONSTRAINT workflows_transition_destination_id_fkey FOREIGN KEY (destination_id) REFERENCES workflows_state(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: workflows_transition_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_transition
    ADD CONSTRAINT workflows_transition_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES permissions_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: workflows_transition_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_transition
    ADD CONSTRAINT workflows_transition_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES workflows_workflow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: workflows_workflowmodelrelation_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_workflowmodelrelation
    ADD CONSTRAINT workflows_workflowmodelrelation_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES workflows_workflow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: workflows_workflowobjectrelation_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_workflowobjectrelation
    ADD CONSTRAINT workflows_workflowobjectrelation_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES workflows_workflow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: workflows_workflowpermissionrelation_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_workflowpermissionrelation
    ADD CONSTRAINT workflows_workflowpermissionrelation_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES permissions_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: workflows_workflowpermissionrelation_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: gf_stage
--

ALTER TABLE ONLY workflows_workflowpermissionrelation
    ADD CONSTRAINT workflows_workflowpermissionrelation_workflow_id_fkey FOREIGN KEY (workflow_id) REFERENCES workflows_workflow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

