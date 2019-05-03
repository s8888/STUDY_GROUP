package elasticsearch.demo;

import java.io.File;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import junit.framework.TestCase;

@SuppressWarnings({ "unchecked", "rawtypes" })
public class AppTest extends TestCase {

	Map map = new HashMap();

	@Override
	protected void setUp() throws Exception {
		map.put("IP", "192.168.99.100"); // TODO
		map.put("PORT", "9200");
		map.put("PIPELINE_NAME", "attachment");
		map.put("INDEX_NAME", "index_aaa");
		map.put("TYPE_NAME", "type_bbb");
		super.setUp();
	}

	public void testApp() throws Exception {

		ElasticSearchAttachmentDemo demo = new ElasticSearchAttachmentDemo(map);
		demo.close();
	}

	public void testCreatePipeline() throws Exception {

		ElasticSearchAttachmentDemo demo = new ElasticSearchAttachmentDemo(map);
		demo.createPipeline();
		demo.close();
	}

	public void testPutFile() throws Exception {

		ElasticSearchAttachmentDemo demo = new ElasticSearchAttachmentDemo(map);
		File file = new File("D://東方金融廣場租賃合同1.docx");
		String id = demo.putAttachmentWithFile(file);
		System.err.println(id);
		demo.close();
	}
	
	public void testQuery() throws Exception {

		ElasticSearchAttachmentDemo demo = new ElasticSearchAttachmentDemo(map);
		List<Map> data = demo.searchFileWithString("keyword"); // TODO
		System.err.println(data);
		demo.close();
	}
	
	public void testDeleteById() throws Exception {

		ElasticSearchAttachmentDemo demo = new ElasticSearchAttachmentDemo(map);
		//TODO  
		demo.close();
	}


}
