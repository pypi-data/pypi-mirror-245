var layerLoadErrorMessages=[];showMessage('Loading',staticTemplates.loadingModal[mode]);
function runGeeViz(){
try{
	Map2.addSerializedLayer({"result": "0", "values": {"0": {"functionInvocationValue": {"functionName": "Image.toArray", "arguments": {"image": {"functionInvocationValue": {"functionName": "Image.float", "arguments": {"value": {"functionInvocationValue": {"functionName": "Image.addBands", "arguments": {"dstImg": {"functionInvocationValue": {"functionName": "Image.constant", "arguments": {"value": {"constantValue": 2.2222222}}}}, "srcImg": {"functionInvocationValue": {"functionName": "Image.constant", "arguments": {"value": {"constantValue": 3.2344444444}}}}}}}}}}}}}}},{"palette": "blue"},'Layer 1',true);
}catch(err){
	layerLoadErrorMessages.push("Error loading: Layer 1<br>GEE "+err);}
try{
	Map2.addSerializedLayer({"result": "0", "values": {"1": {"functionInvocationValue": {"functionName": "Image.select", "arguments": {"bandSelectors": {"constantValue": [0]}, "input": {"argumentReference": "_MAPPING_VAR_0_0"}}}}, "0": {"functionInvocationValue": {"functionName": "Collection.map", "arguments": {"baseAlgorithm": {"functionDefinitionValue": {"argumentNames": ["_MAPPING_VAR_0_0"], "body": "1"}}, "collection": {"functionInvocationValue": {"functionName": "ImageCollection.load", "arguments": {"id": {"constantValue": "USFS/GTAC/LCMS/v2022-8"}}}}}}}}},{"autoViz": true},'Layer 2',true);
}catch(err){
	layerLoadErrorMessages.push("Error loading: Layer 2<br>GEE "+err);}
if(layerLoadErrorMessages.length>0){showMessage("Map.addLayer Error List",layerLoadErrorMessages.join("<br>"));}
setTimeout(function(){if(layerLoadErrorMessages.length===0){$('#close-modal-button').click();}}, 2500);
Map2.setQueryPrecision(4,1e-05);
Map2.turnOnInspector();
queryWindowMode = "sidePane"
}