from email.policy import default
from flask import g, request
from flask_restx import Namespace, Resource, fields
import json
ns = Namespace(
    'atms',
    'Manages directory of ATM machines in Vancouver.'
)

SRID = 4326

geometry = ns.model('Geometry', {
    
    'type': fields.String(required=True, default='', description='Type of the shape'),
    'coordinates': fields.List(fields.Float()),
})

atm = ns.model('InputModel', {
    'address': fields.String(required=True, default='', description='The atm address'),
    'provider': fields.String(required=True, default='', description='Provider name (BANK)'),
    'geometry' : fields.Nested(
            geometry, description='GPS Location'
        )
})

def existAtm(id):
    """exist atm id"""
    query = '''SELECT count(1) FROM atm WHERE id = :id'''
    result = g.db.execute(query, {'id':id})
    row = result.fetchone()
    result.close()
    return row[0] > 0

@ns.route('/')
class AtmList(Resource):
    @ns.doc('list atms')
    def get(self):
        '''List ATMs'''
        query = '''SELECT jsonb_build_object(
						    'id',         id,
						    'geometry',   ST_AsGeoJSON(geom)::jsonb,
						    'address', address,
						    'provider', provider
						    ) AS json 
                    FROM atm'''
        result = g.db.execute(query)
        rows = result.fetchall();
        data = []
        for row in rows:
            data.append(row[0])
        result.close()

        return data, 200

    
    @ns.expect(atm)
    def post(self):
        """Submit a new ATM:"""
        atm = request.get_json()
        query = '''INSERT INTO atm (geom,
                                    bgeom, 
                                    address, 
                                    provider) 
                    VALUES (ST_GeomFromGeoJSON(:geojson),
                            ST_AsBinary(ST_GeomFromGeoJSON(:geojson)),
                            :address, 
                            :provider
                            )  RETURNING id'''

        result = g.db.execute(query, {'geojson':json.dumps(atm['geometry']), 'address':atm['address'], 'provider':atm['provider']})
        atm['id'] = result.fetchone()[0]
        result.close()
        g.db.commit();
        return atm, 201
    

@ns.route('/<int:id>')
@ns.param('id', 'The atm identifier')
class Atm(Resource):
    def get(self, id):
        """Get GeoJson"""
        query = '''SELECT ST_AsGeoJSON(t.*)
                    FROM(SELECT id, 
                                geom,  
                                address, 
                                provider 
                            FROM atm
                            WHERE id=:id) as t (id, geom, address, provider)'''
        result = g.db.execute(query, {'id':id})
        row = result.fetchone()
        result.close()

        print(row)
        if row == None:
            ns.abort(404, "Atm is not exists")
        
        return row[0], 200

@ns.route('/bbox')
class AtmBBox(Resource):
    def get(self):
        """Get Boundary box of All atms"""
        query = '''SELECT ST_AsText(ST_Envelope(ST_Collect( ARRAY( SELECT geom 
                                                                   FROM atm ))))'''
        result = g.db.execute(query)
        row = result.fetchone()
        result.close()
        
        return row[0], 200