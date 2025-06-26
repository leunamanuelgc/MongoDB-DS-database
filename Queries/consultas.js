/*-----------------------------------------------------------------------------------------------------------------------------------------------------*/
/*----------------------------------------------------- 1.CONSULTAS DE FILTRADO -----------------------------------------------------------------------*/
/*-----------------------------------------------------------------------------------------------------------------------------------------------------*/

/*-----------------------------------------------------------------------------------------------------------------------------------------------------*/
/*---------------------------------------------------- 1.1.POR UNA SOLA CONDICIÓN ---------------------------------------------------------------------*/
/*-----------------------------------------------------------------------------------------------------------------------------------------------------*/

/*---- MOSTRAR TODOS LOS ENEMIGOS QUE SON JEFES ----*/
db.enemigos.find({ "es_jefe": "1" })
/*- ÍNDICE -*/
db.enemigos.createIndex({ "es_jefe": -1 })

/*---- MOSTRAR LOS JUGADORES QUE TENGAN EQUIPADA UNA MAGIA DE TIPO MILAGRO ----*/
const start = new Date();
const result = db.jugadores.aggregate([
	{
		$lookup: {
			from: "objetos",
			localField: "hechizo_equipado",
			foreignField: "_hechizo_id",
			as: "hechizo_info"
		}
	},
	{ $unwind: "$hechizo_info" },
	{
		$match: {
			"hechizo_info.tipo": { $regex: /miracle/i } 
		}
	},
	{
		$project: {
			_id: 0,
			nombre: 1,
			hechizo_equipado: 1,
			tipo_hechizo: "$hechizo_info.tipo",
			nombre_hechizo: "$hechizo_info.nombre"
		}
	}
]).toArray();
const end = new Date();
print(`Execution time (VERSION 1): ${end - start} ms`);
printjson(result);
/*- ÍNDICE -*/
db.jugadores.createIndex({ "Jugadores_Con_Milagros_Equipados": 1 })

/*-----------------------------------------------------------------------------------------------------------------------------------------------------*/
/*---------------------------------------------------- 1.2.POR VARIAS CONDICIONES ---------------------------------------------------------------------*/
/*-----------------------------------------------------------------------------------------------------------------------------------------------------*/

/*---- MOSTRAR LOS JEFES CUYAS ALMAS SON MAYORES QUE 50.000 ----*/
db.enemigos.find(
{ $expr: {$and: [ {es_jefe:"1"},
{$gt: [ {$toInt: "$almas"}, 50000]}]}},
{ _id: 0, nombre: 1, almas: 1 })
/*- ÍNDICE -*/
db.enemigos.createIndex({ "es_jefe": 1 })
db.enemigos.createIndex({ "es_jefe": 1, "almas":1 })

/*---- JUGADORES CUYO NOMBRE CONTENGA 'x' (MAYUS O MINUS), QUE TIENEN UN ARMA DE FUEGO Y ESTÁN INVADIENDO A ALGUIEN ----*/
db.jugadores.find({
	$and: [
		{ "nombre": { $regex: /[x]/, $options: "i" } },
		{ "lista_armas.elemento": "Fire" },
		{ "invasion": { $ne: null } }
	]
},
	{ nombre: 1, lista_armas: { $elemMatch: { elemento: "Fire" } }, invasion: 1 })
/*- ÍNDICE -*/
db.jugadores.createIndex({ "invasion": 1 })
db.jugadores.createIndex({ "lista_armas": 1 })
db.jugadores.createIndex({ "nombre": 1 })
db.jugadores.createIndex({ "lista_armas.element": 1 })

/*---- ZONAS CON 3 O MÁS TIPOS DE ENEMIGOS DIFERENTES Y MENOS DE 3 HOGUERAS ----*/
db.zonas.find(
	{
		$and: [
			{ lista_enemigos: { $type: "array" } },
			{ lista_hogueras: { $type: "array" } },
			{ $expr: { $gt: [ {$size: "$lista_enemigos"}, 2 ] } },
			{ $expr: { $lt: [ {$size: "$lista_hogueras"}, 3 ] } }
		]
	},
	{
		nombre: 1
	}
)
/*- ÍNDICE -*/
db.zonas.createIndex({ "lista_enemigos.cantidad": 1 })
db.zonas.createIndex({ "lista_hogueras": 1 })

/*---- ENEMIGOS QUE DAN MUCHAS ALMAS (1000) Y TIENEN POCA VIDA (300) ----*/ 
db.enemigos.find(
	{
		$expr: {
			$and: [
				{ $gte: [{ $toInt: "$almas" }, 1000] },
				{ $lte: [{ $toInt: "$vida" }, 300] }
			]
		}
	},
	{
		_id: 0,
		nombre: 1,
		almas: 1,
		vida: 1
	}
)
/*- ÍNDICE -*/
db.enemigos.createIndex({ "Enemigos_poca_vida_muchas_almas": 1 })

/*-----------------------------------------------------------------------------------------------------------------------------------------------------*/
/*----------------------------------------------------- 2.CONSULTAS DE ORDENACIÓN ---------------------------------------------------------------------*/
/*-----------------------------------------------------------------------------------------------------------------------------------------------------*/

/*---- LAS 5 ARMAS CON MAYOR DURABILIDAD ORDENADAS DE MAYOR A MENOR, MOSTRANDO NOMBRE, TIPO Y DURABILIDAD MÁXIMA ----*/ 
const start = new Date();
const result = db.objetos.aggregate([
	{
		$match: {
			_arma_id: { $regex: /.*/i }
		}
	},
	{
		$addFields: {
			durabilidad_int: { $toInt: "$durabilidad_max" }
		}
	},
	{
		$sort: { durabilidad_int: -1 }
	},
	{
		$limit: 5
	},
	{
		$project: {
			_id: 0,
			nombre: 1,
			tipo: 1,
			durabilidad_max: 1
		}
	}
])
const end = new Date();
print(`Execution time (VERSION 1): ${end - start} ms`);
printjson(result);
/*- ÍNDICE -*/
db.objetos.createIndex({ "top_5_armas_mayor_durabilidad": 1 })

/*---- MOSTRAR LOS JUGADORES CON MAYOR CANTIDAD DE MUERTES, ORDENADOS DE MAYOR A MENOR ----*/
db.jugadores.find({}, { _id: 0, nombre: 1, muertes: 1 }).sort({ muertes: -1 })
/*- ÍNDICE -*/
db.jugadores.createIndex({ "muertes": -1 })
db.jugadores.createIndex({ "muertes": -1, "nombre": 1 })

/*---- MOSTRAR EL NOMBRE DE LOS JUGADORES, SUS ALMAS Y EL PACTO AL QUE PERTENECEN, ORDENADO POR EL NOMBRE DEL JUGADOR ALFABÉTICAMENTE ----*/
db.jugadores.find({}, {_id: 0, nombre: 1, almas: 1, pacto: 1}).sort({nombre: 1}) 
/*- ÍNDICE -*/
db.enemigos.createIndex({ "nombre": 1 })

/*-----------------------------------------------------------------------------------------------------------------------------------------------------*/
/*-------------------------------------------- 3.CONSULTAS NUEVAS CON AGGREGATION FRAMEWORK -----------------------------------------------------------*/
/*-----------------------------------------------------------------------------------------------------------------------------------------------------*/

/*---- TIEMPOS ENTRE MUERTES, HACER LA MEDIA POR CADA JUGADOR Y ORDENARLOS ----*/
const start = new Date();
const result = db.jugadores.aggregate([
	// Tiempo de muerte convertido a ms de juego de cada jugador
	{
		$project: {
			nombre: 1,
			tiempos_muerte_ms: {
				$map: {
					input: "$manchas_sangre",
					as: "mancha",
					in: {
						$let: {
							vars: { parts: { $split: ["$$mancha.tiempo_muerte", ":"] } },
							in: {
								$add: [
									{ $multiply: [{ $toInt: { $arrayElemAt: ["$$parts", 0] } }, 3600000] }, // hours → ms
									{ $multiply: [{ $toInt: { $arrayElemAt: ["$$parts", 1] } }, 60000] },   // minutes → ms
									{ $toInt: { $multiply: [{ $toDouble: { $arrayElemAt: ["$$parts", 2] } }, 1000] } } // seconds (with decimals)
								]
							}
						}
					}
				}
			}
		}
	},
	// Intervalo de tiempo entre cada muerte de cada jugador
	{
		$project: {
			nombre: 1,
			intervalos_muerte: {
				$map: {
					input: { $range: [0, { $size: "$tiempos_muerte_ms" }, 2] },
					as: "index",
					in: { $slice: ["$tiempos_muerte_ms", "$$index", 2] }
				}
			}
		}
	},
	// Media de los intervalos de tiempo entre muertes de cada jugador
	{
		$project: {
			nombre: 1,
			tiempo_vida_medio: {
				$avg: {
					$map: {
						input: "$intervalos_muerte",
						as: "par_muertes",
						in: { $subtract: [{ $arrayElemAt: ["$$par_muertes", 1] }, { $arrayElemAt: ["$$par_muertes", 0] }] }
					}
				}
			}
		}
	},
	// Tiempo medio de vida bien formateado
	{
		$project: {
			nombre: 1,
			tiempo_vida_medio: 1,
			tiempo_vida_medio_formateado: {
				$let: {
					vars: {
						total_ms: "$tiempo_vida_medio",
						horas: { $floor: { $divide: ["$tiempo_vida_medio", 3600000] } },
						minutos: {
							$floor: {
								$divide: [
									{ $mod: ["$tiempo_vida_medio", 3600000] },
									60000
								]
							}
						},
						segundos_decimales: {
							$divide: [
								{ $mod: ["$tiempo_vida_medio", 60000] },
								1000
							]
						}
					},
					in: {
						$concat: [
							// Horas padded to 2 digits
							{
								$cond: [
									{ $lte: ["$$horas", 9] },
									{ $concat: ["0", { $toString: "$$horas" }] },
									{ $toString: "$$horas" }
								]
							},
							":",
							// Minutos padded
							{
								$cond: [
									{ $lte: ["$$minutos", 9] },
									{ $concat: ["0", { $toString: "$$minutos" }] },
									{ $toString: "$$minutos" }
								]
							},
							":",
							// Segundos padded + decimals (always 3 digits for ms)
							{
								$let: {
									vars: {
										seg: { $floor: "$$segundos_decimales" },
										ms: {
											$substrBytes: [
												{
													$concat: [
														{ $toString: { $round: [{ $mod: ["$$segundos_decimales", 60] }, 3] } },
														"000" // padding trick
													]
												},
												0,
												6
											]
										}
									},
									in: {
										$cond: [
											{ $lte: ["$$seg", 9] },
											{ $concat: ["0", "$$ms"] },
											"$$ms"
										]
									}
								}
							}
						]
					}
				}
			}
		}
	},
	// Jugadores ordenados segun su tiempo de vida medio (orden descendente)
	{ $sort: { tiempo_vida_medio: -1 } },
	// _id: 0, -> Si queremos esconder los ids de los jugadores
	{ $project: { _id: 0, nombre: 1, tiempo_vida_medio_formateado: 1 } }
]).toArray();
const end = new Date();
print(`Execution time (VERSION 1): ${end - start} ms`);
printjson(result);
/*- ÍNDICE -*/
db.jugadores.createIndex({ "manchas_sangre.tiempo_muerte": 1 })

/*---- JUGADORES Y SUS EQUIPACIONES(MOSTRAR SUS NOMBRES) ORDENADOS POR EL NÚMERO DE MUERTES DEL JUGADOR (EN ORDEN ASCENDENTE) ----*/
const start = new Date();
const result = db.jugadores.aggregate([
	{
		$lookup: {
			from: "objetos", localField: "arma_equipada", foreignField: "_arma_id", as: "arma"
		}
	},
	{
		$lookup: {
			from: "objetos", localField: "hechizo_equipado", foreignField: "_hechizo_id", as: "hechizo"
		}
	},
	{
		$lookup: {
			from: "objetos", localField: "casco_equipado", foreignField: "_pieza_armadura_id", as: "casco"
		}
	},
	{
		$lookup: {
			from: "objetos", let: { idBuscado: "$torso_equipado" }, pipeline: [{
				$match: {
					$expr: {
						$and: [
							{ $eq: ["$slot_armadura", "Torso"] },
							{ $eq: ["$_pieza_armadura_id", "$$idBuscado"] }
						]
					}
				}
			}], as: "torso"
		}
	},
	{
		$lookup: {
			from: "objetos", let: { idBuscado: "$pernera_equipada" }, pipeline: [{
				$match: {
					$expr: {
						$and: [
							{ $eq: ["$slot_armadura", "Piernas"] },
							{ $eq: ["$_pieza_armadura_id", "$$idBuscado"] }
						]
					}
				}
			}], as: "pernera"
		}
	},
	{
		$lookup: {
			from: "objetos", localField: "guantes_equipado", foreignField: "_pieza_armadura_id", as: "guantes"
		}
	},
	{
		$lookup: { from: "objetos", localField: "item_equipado", foreignField: "_item_id", as: "item" }
	},
	{ $addFields: { "numero_muertes": { $size: "$manchas_sangre" } } },
	{
		$project: {
			jugador: "$nombre", arma: { $arrayElemAt: ["$arma.nombre", 0] }, hechizo: { $arrayElemAt: ["$hechizo.nombre", 0] }, armadura: {
				casco: { $arrayElemAt: ["$casco.nombre", 0] }, torso: { $arrayElemAt: ["$torso.nombre", 0] }, pernera: { $arrayElemAt: ["$pernera.nombre", 0] },
				guantes: { $arrayElemAt: ["$guantes.nombre", 0] }
			}, items: { $arrayElemAt: ["$item.nombre", 0] }, numero_muertes: "$numero_muertes"
		}
	},
	{ $sort: { "numero_muertes": 1 } }
]).toArray();
const end = new Date();
print(`Execution time: ${end - start} ms`);
printjson(result);
/*- ÍNDICE -*/
db.objetos.createIndex({ "_pieza_armadura_id": 1 })
db.objetos.createIndex({ "_item_id": 1 })
db.jugadores.createIndex({ "manchas_sangre": 1 }) //etc.

/*-----------------------------------------------------------------------------------------------------------------------------------------------------*/
/*----------------------------------------------- 4.CONSULTAS DE AGREGACIÓN Y COMBINACIÓN -------------------------------------------------------------*/
/*-----------------------------------------------------------------------------------------------------------------------------------------------------*/

/*---- LOS 7 JUGADORES CON MÁS MAGIAS EN SU POSESIÓN, MOSTRAR SU NOMBRE, ID Y CANTIDAD DE MAGIAS ----*/
db.jugadores.aggregate([ 
{$project: {_id: 1, nombre: 1, cantidad_magias: { $size: "$lista_hechizos" }}}, 
  { $sort: { cantidad_magias: -1 } }, 
  { $limit: 7 } 

/*---- SUMA DEL NÚMERO TOTAL DE ALMAS QUE TE DA CADA TIPO ENEMIGO A LO LARGO DE CADA ZONA ----*/
db.zonas.aggregate(
	[
		{ $unwind: "$lista_enemigos" },
		{
			$lookup: {
				from: "enemigos",
				localField: "lista_enemigos._enemigo_id",
				foreignField: "_enemigo_id",
				as: "info_enemigo"
			}
		},
		{ $unwind: "$info_enemigo" },
		{
			$group: {
				_id: { zona_id: "$_zona_id", enemigo_id: "$info_enemigo._enemigo_id" },
				nombre_zona: { $first: "$nombre" },
				cantidad: { $first: "$lista_enemigos.cantidad" },
				almas_por_enemigo: { $first: "$info_enemigo.almas" },
				almas_totales_zona: {
					$sum: {
						$multiply: [
							{ $toInt: "$info_enemigo.almas" },
							{ $toInt: "$lista_enemigos.cantidad" }
						]
					}
				},
				nombre_enemigo: { $first: "$info_enemigo.nombre" }
			},
		},
		{
			$group: {
				_id: "$_id.zona_id",
				nombre_zona: { $first: "$nombre_zona" },
				enemigos: {
					$push: {
						nombre_enemigo: "$nombre_enemigo",
						cantidad: { $toInt: "$cantidad" },
						almas_por_enemigo: { $toInt: "$almas_por_enemigo" },
						almas_totales: "$almas_totales_zona",
						
					}
				},
				almas_totales_zona: { $sum: "$almas_totales_zona" }
			}
		},
		{ $sort: { "_id": 1 } },
		{ $project:
			{
				_id: 0,
				nombre_zona: 1,
				enemigos: 1,
				almas_totales_zona: 1
			}
		}
	]
)
/*- ÍNDICE -*/
db.enemigos.createIndex({ _enemigo_id: 1 })
db.zonas.createIndex({ "lista_enemigos._enemigo_id": 1 })

/*---- MOSTRAR EL NÚMERO TOTAL DE CADA ENEMIGO CONTANDO DE ZONA EN ZONA ----*/
var start = Date.now(); 
var resultado = db.zonas.aggregate([ 
  { $unwind: "$lista_enemigos" }, 
  { $group: { 
      _id: { zona: "$nombre", enemigoId: "$lista_enemigos._enemigo_id" }, 
      total: { $sum: { $toInt: "$lista_enemigos.cantidad" } } 
  }}, 
  { $lookup: { 
      from:       "enemigos", 
      localField: "_id.enemigoId", 
      foreignField:"_enemigo_id", 
      as:         "detalle" 
  }}, 
  { $unwind: "$detalle" }, 
  { $project: { _id:0, zona:"$_id.zona", enemigo:"$detalle.nombre", total:1 }} 
]).toArray(); 
var end = Date.now(); 
printjson({ tiempo_ms: end - start }); 
printjson(resultado); 