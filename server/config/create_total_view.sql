create view osparc_total as select SUM(dcrating) totaldcrating,SUM(storageoriginalcapacity) totalstoragecapacity from osparc_plant;
