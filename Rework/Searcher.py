import math

class Search:
    
    def __init__(self):
        pass

    def search_urls_from_keywords(self, keywords:list[str], ivi_index:dict):
        results = set()
        for keyword in keywords:
            if keyword in ivi_index:
                for url in ivi_index[keyword]:
                    results.add(url)
        return results
        
    def get_ref_count(self, url, raw_index:dict):
        refcount = 0
        if url in raw_index:
            for key in raw_index:
                if url in raw_index[key]["links"] and key.split("/")[2] != url.split("/")[2]:
                    refcount += 1
        return refcount
    
    def get_locations_from_url(self, url:str, fw_index:dict):
        if url in fw_index:
            return fw_index[url]["Location"]

    def search(self, keywords:list[str], raw_index:dict, fw_index:dict, ivi_index:dict):
        results = []
        urls_hit = self.search_urls_from_keywords(keywords, ivi_index)
        for url in urls_hit:
            ref_count = self.get_ref_count(url, raw_index)
            tf_idf = self.calculate_tf_idf(url, keywords, fw_index, ivi_index)
            score = tf_idf + 0.1 * ref_count / len(fw_index)
            results.append((url, score, ref_count, self.get_locations_from_url(url, fw_index)))
        results.sort(key=lambda x : x[1], reverse=True)
        return results
    
    def calculate_tf_idf(self, url:str, keywords:list[str], fw_index:dict, ivi_index:dict):
        tf, idf = 0, 0
        for keyword in keywords:
            if keyword in fw_index[url]["Keywords"]:
                tf += (ivi_index[keyword][url] / sum([fw_index[url]["Keywords"][key] for key in fw_index[url]["Keywords"]]))
                idf += (math.log(len(fw_index) / len(ivi_index[keyword])))
        tf_idf = tf * idf
        return tf_idf
