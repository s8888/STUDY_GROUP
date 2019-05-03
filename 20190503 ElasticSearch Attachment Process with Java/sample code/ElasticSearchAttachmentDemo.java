package elasticsearch.demo;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Base64;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.apache.commons.collections.MapUtils;
import org.apache.commons.fileupload.FileItem;
import org.apache.commons.io.FileUtils;
import org.apache.commons.io.FilenameUtils;
import org.apache.commons.io.IOUtils;
import org.apache.http.HttpEntity;
import org.apache.http.HttpHost;
import org.apache.http.entity.ContentType;
import org.apache.http.nio.entity.NStringEntity;
import org.apache.http.util.EntityUtils;
import org.elasticsearch.client.Response;
import org.elasticsearch.client.ResponseException;
import org.elasticsearch.client.RestClient;
import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONStringer;
import org.json.JSONWriter;

@SuppressWarnings({ "unchecked", "rawtypes" })
public class ElasticSearchAttachmentDemo {

	private RestClient restClient = null;

	private String ip;// server info
	private int port;// server info
	private String pipelineName;// elastic setting (need only once)
	private String indexName;// index => Database
	private String typeName;// type => Table
	private String endPoint; //  /index/type/ for insert、query
	
	
	/**
	 * Constructor 順便初始化其他需要的參數
	 */
	public ElasticSearchAttachmentDemo(Map map) {	
		 this.setInfoAndBuildClient(map);
	}
	
	private void setInfoAndBuildClient(Map map){

		this.ip = MapUtils.getString(map, "IP"); 
		this.port =MapUtils.getIntValue(map, "PORT");
		this.pipelineName = MapUtils.getString(map, "PIPELINE_NAME"); 
		this.indexName = MapUtils.getString(map, "INDEX_NAME"); 
		this.typeName = MapUtils.getString(map, "TYPE_NAME");
		this.endPoint = new StringBuilder().append('/').append(this.indexName) // index
				.append('/').append(this.typeName) // type
				.append('/').toString();

		restClient = RestClient.builder(
				new HttpHost(this.ip, this.port, "http")).build();
	}

	/**
	 * 產生pipeline(附件搜尋套件目前一定要用pipeline)
	 * @param none  用default
	 */
	public void createPipeline() throws Exception {

		String jsonString = "{"
				+ "\"description\":\"Extract attachment information\","
				+ "\"processors\":[{ \"attachment\": {   \"field\" : \"data\"  }     }]"
				+ "}";
		this.createPipeline(jsonString);
	}

	/**
	 * 產生pipeline(附件搜尋套件目前一定要用pipeline)
	 * 
	 * @param 自定義
	 */
	public void createPipeline(String jsonString) throws Exception {

		System.err.println("jsonString: " + jsonString);

		Map<String, String> params = new HashMap<String, String>();

		HttpEntity entity = new NStringEntity(jsonString,
				ContentType.APPLICATION_JSON);
		Response response = restClient.performRequest("PUT",
				"/_ingest/pipeline/" + this.pipelineName, params, entity);
		this.checkResponse(response);
	}

	/**
	 * @param attachment (FileInputStream) => elasticSearch
	 */
	public String putAttachmentWithFileStream(FileInputStream fileStream)
			throws Exception {

		return this.putAttachmentWithFileStream(fileStream, Collections.EMPTY_MAP);

	}

	/**
	 * @param attachment (FileInputStream) => elasticSearch
	 * @param infoMap (其他想偷藏的資訊，查詢時可以一起取得)
	 */
	public String putAttachmentWithFileStream(FileInputStream fileStream,
			Map infoMap) throws Exception {
	    
	    InputStreamReader reader = new InputStreamReader(fileStream);
		String base64String = Base64.getEncoder().encodeToString(IOUtils
				.toByteArray(reader,reader.getEncoding()));

		return this.putAttachment(base64String, infoMap);

	}
	
	
	/**
	 * @param attachment(FileItem) => elasticSearch
	 */
	public String putAttachmentWithFileItem(FileItem fileItem) throws Exception {

		return this.putAttachmentWithFileItem(fileItem, Collections.EMPTY_MAP);

	}
	
	/**
	 * @param attachment(FileItem) => elasticSearch
	 */
	public String putAttachmentWithFileItem(FileItem fileItem, Map infoMap) throws Exception {

	    InputStreamReader reader = new InputStreamReader(fileItem.getInputStream());
		String base64String = Base64.getEncoder().encodeToString(IOUtils
				.toByteArray(reader,reader.getEncoding()));

		return this.putAttachment(base64String, infoMap);

	}
	
	

	/**
	 * @param attachment(File) => elasticSearch
	 */
	public String putAttachmentWithFile(File file) throws Exception {

		return this.putAttachmentWithFile(file, Collections.EMPTY_MAP);

	}

	/**
	 * @param attachment (File) => elasticSearch
	 * @param infoMap (其他想偷藏的資訊，查詢時可以一起取得) 會額外檢查檔案是否太大
	 */
	public String putAttachmentWithFile(File file, Map infoMap) throws Exception {

		long length = file.length();

		if (length > Integer.MAX_VALUE/10) { // 200 MB
			System.err.println("file length:" + length);
			throw new Exception("File is too large!!!!");
		}

		String fileExt = "doc,docx,xls,xlsx,ppt,pptx,pdf";
		String extension = FilenameUtils.getExtension(file.getPath());
		String base64String = null;
		
		if(fileExt.contains(extension)){
		    base64String = Base64.getEncoder().encodeToString(FileUtils.readFileToByteArray(file));       
		}else{
		    //String encoding = EncodingHelper.isBig5Encoding(file)? "big5":"utf-8";
	        base64String = Base64.getEncoder().encodeToString(FileUtils.readFileToString(file, "utf-8").getBytes());       
		}
		

		return this.putAttachment(base64String, infoMap);

	}

	/**
	 * 將 fileBase64String => elasticSearch 
	 * @param infoMap(其他想偷藏的資訊，查詢時可以一起取得)
	 * @return 
	 */
	private String putAttachment(String fileBase64String, Map<String,Object> infoMap)
			throws Exception {

		JSONWriter writer = new JSONStringer();		
		writer.object()
		      .key("data").value(fileBase64String);
		
		for (String _key : infoMap.keySet()) { // ", "key" : "value" "
			writer.key(_key).value(infoMap.get(_key));
		}
		
		writer.endObject();

		String jsonString = writer.toString();

		HttpEntity entity = new NStringEntity(jsonString,
				ContentType.APPLICATION_JSON);

		Map<String, String> params = new HashMap<String, String>();
		params.put("pipeline", this.pipelineName);

		Response response = restClient.performRequest("POST", this.endPoint,
				params, entity);
		this.checkResponse(response);
		
		String id =this.getElasticId(response);
		return id;
	}

	/**
	 * 查詢
	 * @param keyword 想查詢的關鍵字
	 * @return List<Map> 符合的資料
	 */

	public List<Map> searchFileWithString(String keyword) throws Exception {

	
		String[] keywords = keyword.split(" ");
		JSONWriter writer = new JSONStringer();		
		
		/*
		   {
			  "min_score": length,
			  "query": {
			    "bool": {
			      "should": [
				  
			      ]
			    }
			  }
			}
		*/
		writer.object()
		      .key("min_score").value(keywords.length)
		      .key("query").object()
		                   .key("bool").object()
		                               .key("should").array();
		
		
		
		/* { "constant_score": {
	          "filter": { "match_phrase": { "attachment.content": keyword }}
	        }}
		*/
		for(String str:keywords){
			writer.object()
			      .key("constant_score").object()
			                            .key("filter").object()
			                                          .key("match_phrase").object()
			                                                              .key("attachment.content").value(str)
			                                                              .endObject()
			                                          .endObject()
			                            .endObject()
			      .endObject();                                     
		}
		
		
		//補上結尾 ]}}}
		writer.endArray().endObject().endObject().endObject();                

		return this.search(writer.toString());
	}

	/**
	 * 查詢
	 * @param jsonString 想查詢的json指令
	 * @return List<Map> 符合的資料
	 */
	private List<Map> search(String jsonString) throws Exception {

		System.err.println("jsonString: " + jsonString);

		Map<String, String> params = new HashMap<String, String>();

		HttpEntity entity = new NStringEntity(jsonString,
				ContentType.APPLICATION_JSON);

		Response response = restClient.performRequest("POST", this.endPoint
				+ "_search", params, entity);
		this.checkResponse(response);

		return this.parseResponse(response);
	}

	/**
	 * 解析回傳內容
	 * @param Response response
	 * @return List<Map> 符合的資料
	 */
	private List<Map> parseResponse(Response response) throws Exception {

		List<Map> rtnList = new ArrayList<Map>();

		try {

			String etity_str = EntityUtils.toString(response.getEntity());
			JSONObject jObj = new JSONObject(etity_str);
			JSONArray jArray = jObj.getJSONObject("hits").getJSONArray("hits");// 有命中的

			for (int i = 0; i < jArray.length(); i++) {

				JSONObject obj = jArray.getJSONObject(i);

				Map<String, String> map = new HashMap<String, String>();
				map.put("_id", obj.getString("_id"));

				JSONObject source = obj.getJSONObject("_source");
				Iterator<String> keys = source.keys();

				while (keys.hasNext()) {
					String key = keys.next();
					if (!key.equals("attachment") && !key.equals("data")) {
						map.put(key, source.getString(key));
					}
				}

				rtnList.add(map);
			}
		} catch (Exception e) {
			System.err.println(EntityUtils.toString(response.getEntity()));
			throw new Exception("parse response error", e);
		}

		return rtnList;
	}

	/**
	 * 先一個個刪除，之後再加上 delete by query //TODO
	 * @throws Exception
	 */
	public void deleteDataById(String id) throws Exception {

		try {

			
			//TODO
			Response response = restClient.performRequest("DELETE",
					this.endPoint + id, null, null);
			
			
		} catch (ResponseException re) {

			System.err.println(re.getMessage());
			int status = re.getResponse().getStatusLine().getStatusCode();
			if (status == 404) {// 此id無資料
				throw new Exception(id);
			}

			throw re;
		}

	}

	public void close() throws IOException {
		restClient.close();
	}

	private void checkResponse(Response response) throws Exception {

		int status = response.getStatusLine().getStatusCode();

		if (status >= 300) {
			System.err.println(response.getRequestLine());
			if (status >= 400) {
				System.err.println(status);
				System.err.println(EntityUtils.toString(response.getEntity()));
				throw new Exception("execute error");
			}
		}

	}
	
	/**
	 *  put File 後取得真實id
	 */
	private String getElasticId(Response response) throws Exception{
	    
        String etity_str = EntityUtils.toString(response.getEntity());
        JSONObject jObj = new JSONObject(etity_str);
        return jObj.getString("_id");
	}

}
