CREATE TABLE subscription(
	name varchar(255),
	id varchar(255),
	status varchar(255),
	scope varchar(255),
	tags varchar(5000),
	locks varchar(5000),
	total_rg int,
	unique_rg_loc int,
	rg_loc varchar(5000),
	total_resource int,
	unique_resource_loc int,
	resource_loc varchar(5000),
	current_cost decimal(38,2),
	forecast_cost decimal(38,2),
	non_compliant_resources int,
	non_compliant_policy int,
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE resource_group (
	sub varchar(255),
	name varchar(255),
	location varchar(255),
	provisioning_state varchar(255),
	id varchar(5000),
	tags varchar(5000),
	locks varchar(5000),
	total_resource int,
	unique_resource_loc int,
	resource_loc varchar(5000),
	current_cost decimal(38,2),
	forecast_cost decimal(38,2),
	non_compliant_resources int,
	non_compliant_policy int,
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE resource (
	sub varchar(255),
	name varchar(255),
	location varchar(255),
	rg_name varchar(255),
	type varchar(1000)
	scope varchar(5000),
	tags varchar(5000),
	locks varchar(5000),
	non_compliant_policy int,
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE resource_type_summary (
	sub varchar(255),
	type varchar(5000),
	num int,
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE vm_general (
	sub varchar(255),
	name varchar(255),
	id varchar(5000),
	location varchar(255),
	rg_name varchar(255),
	status varchar(255),
	creation_date DATE,
	size varchar(255),
	os_publisher varchar(255),
	os_offer varchar(255),
	os_sku varchar(255),
	os_version varchar(255),
	os_exact_version varchar(255),
	os_patch_mode varchar(255) DEFAULT NULL,
	os_automatic_update varchar(255) DEFAULT NULL,
	boot_diag_settings varchar(255),
	boot_diag_setting_uri varchar(1000),
	extension_num int,
	extension_names varchar(255) DEFAULT NULL,
	os_disk_name varchar(255),
	os_disk_location varchar(255),
	os_disk_sku_name varchar(255),
	os_disk_sku_tier varchar(255),
	os_disk_size_gb int,
	os_disk_status varchar(255),
	num_data_disk int,
	num_ni int,
	tags varchar(255),
	locks varchar(255),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE vm_data_disk (
	sub varchar(255),
	vm_rg_name varchar(255),
	vm_name varchar(255),
	disk_rg_name varchar(255),
	disk_name varchar(255),
	disk_location varchar(255),
	disk_size_gb int,
	disk_provisioning_state varchar(255),
	disk_state varchar(255),
	disk_sku_name varchar(255),
	disk_sku_tier varchar(255),
	disk_nap varchar(255),
	disk_pub_access_policy varchar(255),
	disk_encryption varchar(255),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE vm_network_interfaces (
	sub varchar(255),
	vm_rg_name varchar(255),
	vm_name varchar(255),
	ni_name varchar(255),
	ni_rg_name varchar(255),
	ni_primary varchar(255),
	ni_location varchar(255),
	ni_provisioning_state varchar(255),
	ni_accelarated_networking varchar(255),
	ni_vnet_encryption varchar(255),
	ni_ip_forwarding varchar(255),
	ni_nsg_name varchar(255),
	ni_nsg_rg_name varchar(255),
	ni_ip_config_name varchar(255),
	ni_ip_config_rg_name varchar(255),
	ni_ip_config_state varchar(255),
	ni_private_ip varchar(255),
	ni_dns_server varchar(255)
	ni_private_ip_allocation varchar(255),
	ni_ip_primary varchar(255),
	ni_private_ip_version varchar(255),
	ni_vnet_rg_name varchar(255),
	ni_vnet_name varchar(255),
	ni_subnet_name varchar(255),
	ni_pip_rg_name varchar(255),
	ni_pip_name varchar(255),
	ni_pip_location varchar(255),
	ni_pip_state varchar(255),
	ni_pip_fqdn varchar(1000),
	ni_pip_address varchar(255),
	ni_pip_version varchar(255),
	ni_pip_allocation varchar(255),
	ni_pip_sku_name varchar(255),
	ni_pip_sku_tier varchar(255),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE vn(
	sub varchar(255),
	rg_name varchar(255),
	name varchar(255),
	location varchar(255),
	provisioning_state varchar(255),
	ddos_protection varchar(255),
	address_space varchar(255),
	dns_servers varchar(255),
	total_subnets int,
	total_peering int,
	tags varchar(5000),
	locks varchar(5000),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE subnet(
	sub varchar(255),
	rg_name varchar(255),
	vnet_name varchar(255),
	name varchar(255),
	provisioning_state varchar(255),
	address_space varchar(255),
	nsg_name varchar(255),
	udr_name varchar(255),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE peering(
	sub varchar(255),
	source_vnet_rg_name varchar(255),
	source_vnet_name varchar(255),
	peering_name varchar(255),
	dest_vnet_name varchar(255),
	dest_vnet_rg_name varchar(255),
	peering_status varchar(255),
	forward_traffic varchar(255),
	gateway_transit varchar(255),
	network_access varchar(255),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE nsg(
	sub varchar(255),
	rg_name varchar(255),
	name varchar(255),
	associated_subnet varchar(255),
	rule_name varchar(255),
	priority int,
	direction varchar(255),
	access varchar(255),
	protocol varchar(255),
	source_port_range varchar(255),
	destination_port_range varchar(255),
	source_address_prefix varchar(255),
	source_port_ranges varchar(255),
	destination_port_ranges varchar(255),
	source_address_prefixes varchar(255),
	destination_address_prefixes varchar(255),
	provisioning_state varchar(255),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE udr(
	sub varchar(255),
	rg_name varchar(255),
	route_table_name varchar(255),
	associated_subnet varchar(255),
	route_name varchar(255),
	address_prefix varchar(255),
	next_hop_type varchar(255),
	next_hop_ip_address varchar(255),
	bgp_overrides varchar(255),
	provisioning_state varchar(255),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE pip(
	sub varchar(255),
	rg_name varchar(255),
	pip_name varchar(255), 
	pip_location varchar(255),
	pip_used varchar(255),
	pip_provisioning_state varchar(255),
	pip_version varchar(255),
	pip_allocation varchar(255),
	pip_sku_name varchar(255),
	pip_sku_tier varchar(255),
	pip_idle_timeout_min int,
	pip_ddos_mode varchar(255),
	pip_fqdn varchar(512),
	tags varchar(5000),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE sa(
	sub varchar(255),
	rg_name varchar(255),
	name varchar(255),
	location varchar(255),
	kind varchar(255),
	sku_name varchar(255),
	sku_tier varchar(255),
	tls_version varchar(255),
	blob_public_access varchar(255),
	access_tier varchar(255),
	num_container int,
	num_file_share int,
	num_tables int,
	num_queues int,
	provisioning_state varchar(255),
	tags varchar(5000),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE blob(
	sub varchar(255),
	rg_name varchar(255),
	sa_name varchar(255),
	name varchar(255),
	deleted varchar(255),
	versioning varchar(255),
	public_access varchar(255),
	lease_status varchar(255),
	lease_state varchar(255),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE file_share(
	sub varchar(255),
	rg_name varchar(255),
	sa_name varchar(255),
	name varchar(255),
	quota_in_gb decimal(38,2),
	protocol varchar(255),
	lease_status varchar(255),
	lease_state varchar(255),
	access_tier varchar(255),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE tables(
	sub varchar(255),
	rg_name varchar(255),
	sa_name varchar(255),
	name varchar(255),
	table_name varchar(255),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE queue(
	sub varchar(255),
	rg_name varchar(255),
	sa_name varchar(255),
	name varchar(255),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE policy_assignments(
	sub varchar(255),
	name varchar(5000),
	enforcement varchar(255),
	location varchar(255),
	scope varchar(5000),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE policy_assessment(
	sub varchar(255),
	assessment_id varchar(255),
	name varchar(10000),
	status varchar(255),
	source varchar(255),
	resource_id varchar(5000),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE aar(
	sub varchar(255),
	impacted_resource varchar(255),
	resource_type varchar(255),
	category varchar(255),
	impact varchar(255),
	problem text,
	solution text,
	resource_id varchar(5000),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE rcs(
	sub varchar(255),
	name varchar(255),
	status varchar(255),
	passed_controls int,
	failed_controls int,
	skipped_controls int,
	unsupported_controls int,
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE rcc(
	sub varchar(255),
	compliance_name varchar(255),
	control_name varchar(255),
	description varchar(5000),
	status varchar(255),
	passed_assessment int,
	failed_assessment int,
	skipped_assessment int,
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE vm_metrics(
	sub varchar(255),
	rg_name varchar(255),
	vm_name varchar(255),
	metrics_name varchar(255),
	metrics_description text,
	timestamp DATETIME,
	minimum decimal(38,2),
	average decimal(38,2),
	maximum decimal(38,2),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE sql_srv(
	sub varchar(255),
	rg_name varchar(255),
	name varchar(255),
	location varchar(255),
	kind varchar(255),
	version varchar(255),
	status varchar(255),
	fqdn varchar(512),
	public_network_access varchar(255),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE sql_dbs(
	sub varchar(255),
	rg_name varchar(255),
	srv_name varchar(255),
	name varchar(255),
	location varchar(255),
	status varchar(255),
	max_size_gb decimal(38,2),
	collation varchar(512),
	zone_redundancy varchar(255),
	creation_date datetime,
	sku_name varchar(255),
	sku_tier varchar(255),
	sku_capacity int,
	read_scale varchar(255),
	backup_storage_redundancy varchar(255),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE sql_fwr(
	sub varchar(255),
	rg_name varchar(255),
	srv_name varchar(255),
	name varchar(255),
	start_ip_address varchar(255),
	end_ip_address varchar(255),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE sql_va(
	sub varchar(255),
	rg_name varchar(255),
	srv_name varchar(255),
	db_name varchar(255),
	assessment_name varchar(255),
	assessment_status varchar(255),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE sql_vas(
	sub varchar(255),
	rg_name varchar(255),
	srv_name varchar(255),
	db_name varchar(255),
	assessment_name varchar(255),
	assessment_status varchar(255),
	scan_name varchar(255),
	scan_id varchar(255),
	status varchar(255),
	trigger_type varchar(255),
	hs_failed_rules int,
	ms_failed_rules int,
	ls_failed_rules int,
	passed_rules int,
	failed_rules int,
	total_rules int,
	baseline_applied varchar(255),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE sql_vasr(
	sub varchar(255),
	rg_name varchar(255),
	srv_name varchar(255),
	db_name varchar(255),
	assessment_name varchar(255),
	assessment_status varchar(255),
	scan_name varchar(255),
	scan_id varchar(255),
	rule_name varchar(255),
	rule_id varchar(255),
	rule_status varchar(255),
	rule_severity varchar(255),
	rule_category varchar(255),
	rule_type varchar(255),
	rule_title text,
	rule_description text,
	rule_remediation text,
	rule_error_message text,
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE sqlmi_srv(
	sub varchar(255),
	rg_name varchar(255),
	name varchar(255),
	location varchar(255),
	status varchar(255),
	provisioning_state varchar(255),
	sku_name varchar(255),
	sku_tier varchar(255),
	sku_family varchar(255),
	sku_capacity int,
	fqdn varchar(1024),
	licence_type varchar(255),
	storage_account_type varchar(255),
	storage_size int,
	collation varchar(255),
	public_endpoint_enabled varchar(255),
	private_endpoint_connection int,
	tls_version varchar(255),
	aad_authentication varchar(255),
	tags text,
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE sqlmi_dbs(
	sub varchar(255),
	rg_name varchar(255),
	srv_name varchar(255),
	name varchar(255),
	location varchar(255),
	status varchar(255),
	collation varchar(512),
	creation_date datetime,
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE df(
	sub varchar(255),
	rg_name varchar(255),
	name varchar(255),
	location varchar(255),
	provisioning_state varchar(255),
	public_network_access varchar(255),
	tags varchar(5000),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE dfds(
	sub varchar(255),
	rg_name varchar(255),
	df_name varchar(255),
	name varchar(255),
	type varchar(255),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE dfp(
	sub varchar(255),
	rg_name varchar(255),
	df_name varchar(255),
	name varchar(255),
	description text,
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE dfpr(
	sub varchar(255),
	rg_name varchar(255),
	df_name varchar(255),
	pipeline_name varchar(255),
	run_id varchar(255),
	run_start varchar(255),
	run_end varchar(255),
	run_duration int,
	run_status varchar(255),
	message text,
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE kv_active(
	sub varchar(255),
	rg_name varchar(255),
	kv_name varchar(255),
	kv_location varchar(255),
	kv_provisioning_state varchar(255),
	kv_public_network_access varchar(255),
	kv_access_policy_num int,
	kv_sku_family varchar(255),
	kv_sku_name varchar(255),
	kv_created_by varchar(255),
	kv_created_at varchar(255),
	kv_last_modified_by varchar(255),
	kv_last_modified_at varchar(255),
	kv_deployment_enabled varchar(255),
	kv_disk_encryption_enabled varchar(255),
	kv_template_deployment_enabled varchar(255),
	kv_soft_delete_enabled varchar(255),
	kv_soft_delete_retension_days int,
	kv_rbac_auth_enabled varchar(255),
	kv_vault_uri varchar(512),
	tags varchar(5000),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE kv_deleted(
	sub varchar(255),
	rg_name varchar(255),
	kv_name varchar(255),
	kv_location varchar(255),
	kv_deletion_date varchar(255),
	kv_purge_date varchar(255),
	kv_purge_protection varchar(255),
	kv_vault_id varchar(255),
	tags varchar(5000),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE lb(
	sub varchar(255),
	rg_name varchar(255),
	lb_name varchar(255),
	lb_location varchar(255),
	lb_provisioning_state varchar(255),
	lb_sku_name varchar(255),
	lb_sku_tier varchar(255),
	lb_frontend_ip_config int,
	lb_backend_address_pool int,
	lb_rules int,
	lb_health_probes int,
	lb_inbound_nat_rules int,
	lb_outbound_rules int,
	lb_inbound_nat_pools int,
	tags varchar(5000),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE lb_fip(
	sub varchar(255),
	rg_name varchar(255),
	lb_name varchar(255),
	fip_name varchar(255),
	fip_type varchar(255),
	fip_provisioning_state varchar(255),
	fip_private_ip varchar(255),
	fip_vn varchar(255),
	fip_subnet varchar(255),
	fip_pip varchar(255),
	fip_outbound_rules_no int,
	fip_lb_rules_no int,
	fip_inbound_nat_rules_no int,
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE ag(
	sub varchar(255),
	rg_name varchar(255),
	ag_name varchar(255),
	ag_location varchar(255),
	ag_provisioning_state varchar(255),
	ag_operational_state varchar(255),
	ag_http2_status varchar(255),
	ag_sku_name varchar(255),
	ag_sku_tier varchar(255),
	ag_sku_capacity varchar(255),
	ag_firewall_status varchar(255),
	ag_firewall_mode varchar(255),
	ag_firewall_rule_set varchar(255),
	ag_firewall_rule_version varchar(255),
	ag_ssl_certificate varchar(255),
	tags varchar(5000),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE vmss(
	sub varchar(255),
	rg_name varchar(255),
	vmss_name varchar(255),
	vmss_location varchar(255),
	vmss_provisioning_state varchar(255),
	vmss_sku_name varchar(255),
	vmss_sku_tier varchar(255),
	vmss_sku_capacity int,
	vmss_fault_domain_count int,
	vmss_upgrade_policy varchar(255),
	vmss_creation_time varchar(255),
	tags varchar(5000),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);

CREATE TABLE vmss_vm(
	sub varchar(255),
	rg_name varchar(255),
	vmss_name varchar(255),
	vm_name varchar(255),
	vm_location varchar(255),
	vm_sku_name varchar(255),
	vm_sku_tier varchar(255),
	vm_size varchar(255),
	vm_os_publisher varchar(255),
	vm_os_offer varchar(255),
	vm_os_sku varchar(255),
	vm_os_version varchar(255),
	vm_os_exact_version varchar(255),
	tags varchar(5000),
	date_of_report DATE NOT NULL DEFAULT GETUTCDATE()
);