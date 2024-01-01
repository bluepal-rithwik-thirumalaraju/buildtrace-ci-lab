# Current client contract

The bundled wirekit wheel must match context/deployment.json. The
project requirement and CI constraint must both admit that major.
The v1 and v2 client constructors are incompatible. This deployment
does not include dependency source or migration notes; CI failures
and the wheel are the available current observations.

Pagination stops only at null, including when a cursor is zero.
Decode JSON with the declared Content-Type charset, default UTF-8.
Retain error response status even when a Response is false in a
boolean context. A 304 reuses cached data; a 200 replaces it.
All other application behavior follows the protected public tests.
