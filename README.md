# UrtheCast/ATM
EarthDaily Home Assignment.

## Environments
- python3.10
- postgis
- Flask2.1.1
- flask-restx0.5.1
- AWS ALB + EC2

## RestAPI Document
-http://krealtors-alb01-2008996948.us-west-1.elb.amazonaws.com:5000/docs

## ATM Table Info

```sql
CREATE TABLE public.atm (
	id serial4 NOT NULL,
	address varchar(256) NOT NULL,
	provider varchar(128) NOT NULL,
	geom public.geometry NOT NULL, /*geometry field*/
	bgeom bytea NULL, /*binary geometry field*/
	CONSTRAINT atm_pkey PRIMARY KEY (id)
);
```


