from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa CORS
from methods.simplex import simplex
from methods.gran_m import gran_m
from methods.dos_fases import dos_fases
app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

###################### SIMPLEX ###########################################
@app.route('/simplex', methods=['POST'])
def resolver_simplex():
    try:
        data = request.json
        funcion_objetivo = data['funcion_objetivo']
        restricciones_coeficientes = data['restricciones_coeficientes']
        restricciones_valores = data['restricciones_valores']

        # Validar datos
        if not funcion_objetivo or not restricciones_coeficientes or not restricciones_valores:
            return jsonify({"error": "Datos incompletos"}), 400

        # Resolver el problema
        resultado = simplex(funcion_objetivo, restricciones_coeficientes, restricciones_valores)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


################### METODO GRAN M ###################################
@app.route('/gran-m', methods=['POST'])
def resolver_gran_m():
    try:
        data = request.json
        tipo_optimizacion = data['tipo_optimizacion']
        funcion_objetivo = data['funcion_objetivo']
        restricciones_coeficientes = data['restricciones_coeficientes']
        restricciones_signos = data['restricciones_signos']
        restricciones_valores = data['restricciones_valores']

        # Validar datos
        if not funcion_objetivo or not restricciones_coeficientes or not restricciones_signos or not restricciones_valores:
            return jsonify({"error": "Datos incompletos"}), 400

        # Resolver el problema
        resultado = gran_m(tipo_optimizacion, funcion_objetivo, restricciones_coeficientes, restricciones_signos,
                           restricciones_valores)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

######################### METODD DOS FASES ##################################
@app.route('/dos-fases', methods=['POST'])
def resolver_dos_fases():
    try:
        data = request.json
        tipo_optimizacion = data['tipo_optimizacion']
        funcion_objetivo = data['funcion_objetivo']
        restricciones_coeficientes = data['restricciones_coeficientes']
        restricciones_signos = data['restricciones_signos']
        restricciones_valores = data['restricciones_valores']

        # Validar datos
        if not funcion_objetivo or not restricciones_coeficientes or not restricciones_signos or not restricciones_valores:
            return jsonify({"error": "Datos incompletos"}), 400

        # Resolver el problema
        resultado = dos_fases(tipo_optimizacion, funcion_objetivo, restricciones_coeficientes, restricciones_signos,
                              restricciones_valores)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

######################## METODO DUAL #########################################



################ EJECUCION DE PROGRAMA ######################################
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)