import logging
from pprint import pprint

logger = logging.getLogger("parser")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

class Parser(object):
    def __init__(self,
            discard_title=True, 
            report_interval=1000,
            delimiter=',',
            ):
        self.discard_title = discard_title
        self.report_interval = report_interval
        self.delimiter = delimiter
        
    def load_as_dict(self, filename, ind_col=[0], extract_col=[1], max_lines=None):
        logger.debug("Load data from %s" % filename)
        d = {}
        f = open(filename, 'r')
        count = 0
        item_count = 0
        line = self.get_next_line(f)
        if self.discard_title:
            line = self.get_next_line(f)
        while line:
            count += 1
            line = self.pre_process(line)
            parts = self.split_to_parts(line)
            if not self.line_sanity_check(parts):
                logger.warning("[SANITY_CHECK_FAIL] %s" % line)
                logger.warning("[SANITY_CHECK_FAIL] %s" % parts)
            else:
                key = []
                val = []
                for i in ind_col:
                    key.append(parts[i])
                for i in extract_col:
                    val.append(parts[i])
                val = tuple(val)
                self.store_to_dict(d, key, val)
                item_count += 1
            line = self.get_next_line(f)
            if count % self.report_interval == 0:
                logger.debug("Finished %d lines" % count)
            if max_lines and count >= max_lines:
                break;
        f.close()
        logger.info("Read %d items from %s" % (item_count, filename))
        return d

    def load_as_list(self, filename, ind_col=0, max_lines=None):
        logger.debug("Load data from %s" % filename)
        l = []
        f = open(filename, 'r')
        count = 0
        item_count = 0
        line = self.get_next_line(f)
        if self.discard_title:
            line = self.get_next_line(f)
        while line:
            count += 1
            line = self.pre_process(line)
            parts = self.split_to_parts(line)
            if not self.line_sanity_check(parts):
                logger.warning("[SANITY_CHECK_FAIL] %s" % line)
                logger.warning("[SANITY_CHECK_FAIL] %s" % parts)
            else:
                key = parts[ind_col]
                val = tuple(parts)
                self.store_to_list(l, key, val)
                item_count += 1
            line = self.get_next_line(f)
            if count % self.report_interval == 0:
                logger.debug("Finished %d lines" % count)
            if max_lines and count >= max_lines:
                break;
        f.close()
        logger.info("Read %d items from %s" % (item_count, filename))
        return l

    def load_rows_yield(self, filename, extract_col, max_lines = None):
        logger.debug("Load data from %s" % filename)        
        f = open(filename, 'r')
        count = 0
        line = self.get_next_line(f)
        if self.discard_title:
            line = self.get_next_line(f)
        while line:
            count += 1
            line = self.pre_process(line)
            parts = self.split_to_parts(line)
            if not self.line_sanity_check(parts):
                logger.warning("[SANITY_CHECK_FAIL] %s" % line)
                logger.warning("[SANITY_CHECK_FAIL] %s" % parts)
            else:
                row = []
                for i in extract_col:
                    row.append(parts[i])
                row = tuple(row)
                yield row
            line = self.get_next_line(f)
            if count % self.report_interval == 0:
                logger.debug("Finished %d lines" % count)
            if max_lines and count >= max_lines:
                break;
        f.close()

    def load_rows(self, filename, extract_col, max_lines = None):
        logger.debug("Load data from %s" % filename)
        l = []
        f = open(filename, 'r')
        count = 0
        line = self.get_next_line(f)
        if self.discard_title:
            line = self.get_next_line(f)
        while line:
            count += 1
            line = self.pre_process(line)
            parts = self.split_to_parts(line)
            if not self.line_sanity_check(parts):
                logger.warning("[SANITY_CHECK_FAIL] %s" % line)
                logger.warning("[SANITY_CHECK_FAIL] %s" % parts)
            else:
                row = []
                for i in extract_col:
                    row.append(parts[i])
                row = tuple(row)
                l.append(row)
            line = self.get_next_line(f)
            if count % self.report_interval == 0:
                logger.debug("Finished %d lines" % count)
            if max_lines and count >= max_lines:
                break;
        f.close()
        return l

    def get_next_line(self, f):
        return f.readline()

    def pre_process(self, line):
        return line

    def split_to_parts(self, line):
        return line.strip(' \r\n').split(self.delimiter)

    def line_sanity_check(self, parts):
        return True

    def get_key(self, key):
        """
        With only one level of key-value dict, lookup becomes super slow when indexed items reach 20k.
        So use two levels of keys.
        """
        composite = ""
        for k in key:
            composite = composite+str(k)
        if len(composite) < 4:
            composite = "####"+composite
        return (composite[0:2], composite[2:4], composite)

    def store_to_list(self, l, key, val):
        index = 0
        try:
            index = int(key)
            while len(l) <= index:
                l.append([])
            l[index].append(val)
        except:
            logger.warning("[STORE_TO_LIST_FAIL] %s" % str(val))
    
    def retrieve_from_list(self, l, key):
        index = 0
        try:
            index = int(key)
            if len(l) > index:
                return l[index]
            return None
        except:
            return None

    def store_to_dict(self, dic, key, val):
        dd = dic
        kk = self.get_key(key)
        for k in kk[0:-1]:
            if k not in dd.keys():
                dd[k] = {}
            dd = dd[k]
        if kk[-1] not in dd.keys():
            dd[kk[-1]] = []
        dd[kk[-1]].append(val)

    def retrieve_from_dict(self, dic, key):
        dd = dic
        kk = self.get_key(key)
        for k in kk[0:-1]:
            if k not in dd.keys():
                return None
            dd = dd[k]
        if kk[-1] not in dd:
            return None
        return dd[kk[-1]]

    def lowest_level_keys(self, dic):
        dd = [dic]
        for i in range(len(self.get_key(("test_key")))-1):
            vals = sum([ddd.values() for ddd in dd], [])
            dd = vals
        return sum([ddd.keys() for ddd in dd], [])
