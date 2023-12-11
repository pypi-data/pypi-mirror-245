from src.python_fireapi_cownex import exception, utils
from src.python_fireapi_cownex.api.base import FireAPI


class Domain(FireAPI):
    """Class for interacting with the Dpmain Endpoints"""

    def list_all_domains(self):
        """List all purchased Domains"""
        return self.request("domain/list", "GET")

    def register_domain(self, domain, handle, authcode=None):
        """
        Register/Transfer a Domain
        :param domain: Domain (ex. fireapi.de)
        :param handle: Previously created handle
        :param authcode: If transfer, authcode
        """
        if not domain or not handle:
            raise exception.ParameterNotGivenException
        data = {"domain": domain, "handle": handle}
        utils.update_json(data, "authcode", authcode)
        return self.request("domain/register", "POST", data)

    def delete_domain(self, domain):
        """
        Deletes the Domain
        :param domain: Domain (ex. fireapi.de)
        """
        if not domain:
            raise exception.ParameterNotGivenException
        return self.request(f"domain/{domain}/delete", "DELETE")

    def undelete_domain(self, domain):
        """
        Undeletes the Domain
        :param domain: Domain (ex. fireapi.de)
        """
        if not domain:
            raise exception.ParameterNotGivenException
        return self.request(f"domain/{domain}/undelete", "POST")

    def get_authcode(self, domain):
        """
        Requests the Authcode
        :param domain: Domain (ex. fireapi.de)
        """
        return self.request(f"domain/{domain}/authcode", "POST")

    def domain_info(self, domain):
        """
        List Info about Domain
        :param domain: Domain (ex. fireapi.de)
        """
        return self.request(f"domain/{domain}/info", "GET")

    def check_domain_available(self, domain):
        """
        Check if Domain can be Register/Transfer
        :param domain: Domain (ex. fireapi.de)
        """
        return self.request(f"domain/{domain}/check", "GET")

    def change_nameserver(self, domain, ns1, ns2, ns3=None, ns4=None, ns5=None):
        """

        :param domain: Domain (ex. fireapi.de)
        :param ns1: Namserver 1 (required)
        :param ns2: Namserver 2 (required)
        :param ns3: Namserver 3 (optional)
        :param ns4:  Namserver 4 (optional)
        :param ns5:  Namserver 5(optional)
        """
        if None in [ns1, ns2]:
            raise exception.ParameterNotGivenException
        data = {"ns1": ns1, "ns2": ns2}
        utils.update_json(data, "ns3", ns3)
        utils.update_json(data, "ns4", ns4)
        utils.update_json(data, "ns5", ns5)
        return self.request(f"domain/{domain}/nameserver", "POST", data)


    def get_pricing(self):
        """Get Domain TLD Pricing"""
        return self.request("domain/pricing", "GET")

    def create_dns_entry(self, domain, type, name, dns_data):
        """
        Create a DNS Entry for given Domain
        :param domain: Domain (ex. fireapi.de)
        :param type: DNS Type
        :param name: Hostname
        :param dns_data: DNS Data
        """
        if None in [domain, type, name, dns_data]:
            raise exception.ParameterNotGivenException
        data = {"type": type, "name": name, "data": dns_data}
        return self.request(f"domain/{domain}/dns/add", "POST", data)

    def get_dns_entry(self, domain):
        """
        List DNS Entrys
        :param domain: Domain (ex. fireapi.de)
        """
        return self.request(f"domain/{domain}/dns", "GET")

    def delete_dns_entry(self, domain, record_id):
        """
        Deletes given DNS-Record
        :param domain: Domain (ex. fireapi.de)
        :param record_id: ID of DNS-Record
        :return:
        """
        data = {"record_id": record_id}
        return self.request(f"domain/{domain}/dns/remove", "DELETE", data)

    def edit_dns_entry(self, domain, record_id, dns_data, type, name):
        """
        Deletes given DNS-Record
        :param domain: Domain (ex. fireapi.de)
        :param record_id: ID of DNS-Record
        :param type: DNS Type
        :param name: Hostname
        :param dns_data: DNS Data
        :return:
        """
        if not utils.is_not_all_none(dns_data, type, name):
            raise exception.OneOptionalParameterRequiredException
        data = {"record_id": record_id}
        utils.update_json(data, "data", dns_data)
        utils.update_json(data, "type", type)
        utils.update_json(data, "name", name)
        return self.request(f"domain/{domain}/dns/edit", "POST", data)

    def create_handle(self, gender, firstname, lastname, street, number, zipcode, city, region, countrycode, email):
        """
        Creates a new Handle
        """
        data = {
            "gender": gender,
            "firstname": firstname,
            "lastname": lastname,
            "street": street,
            "number": number,
            "zipcode": zipcode,
            "city": city,
            "region": region,
            "countrycode": countrycode,
            "email": email
        }
        return self.request("domain/handle/create", "PUT", data)

    def update_handle(self, handle, gender=None, street=None, number=None, zipcode=None, city=None, region=None, countrycode=None, email=None):
        """
        Updates given Handle
        """
        if not utils.is_not_all_none(gender, street, number, zipcode, city, region, countrycode, email):
            raise exception.OneOptionalParameterRequiredException
        data = {}
        utils.update_json(data, "gender", gender)
        utils.update_json(data, "street", street)
        utils.update_json(data, "number", number)
        utils.update_json(data, "zipcode", zipcode)
        utils.update_json(data, "city", city)
        utils.update_json(data, "region", region)
        utils.update_json(data, "countrycode", countrycode)
        utils.update_json(data, "email", email)
        return self.request(f"domain/handle/{handle}/update", "POST", data)

    def handle_details(self, handle):
        """
        Get Handle details
        :param handle: Handle ID
        """
        return self.request(f"domain/handle/{handle}/info", "GET")

    def get_country_codes(self):
        """
        Get Countrycodes for Handle
        """
        return self.request(f"domain/handle/countries", "GET")



