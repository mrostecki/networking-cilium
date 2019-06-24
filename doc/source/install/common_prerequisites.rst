Prerequisites
-------------

Before you install and configure the networking-cilium service,
you must create a database, service credentials, and API endpoints.

#. To create the database, complete these steps:

   * Use the database access client to connect to the database
     server as the ``root`` user:

     .. code-block:: console

        $ mysql -u root -p

   * Create the ``networking_cilium`` database:

     .. code-block:: none

        CREATE DATABASE networking_cilium;

   * Grant proper access to the ``networking_cilium`` database:

     .. code-block:: none

        GRANT ALL PRIVILEGES ON networking_cilium.* TO 'networking_cilium'@'localhost' \
          IDENTIFIED BY 'NETWORKING_CILIUM_DBPASS';
        GRANT ALL PRIVILEGES ON networking_cilium.* TO 'networking_cilium'@'%' \
          IDENTIFIED BY 'NETWORKING_CILIUM_DBPASS';

     Replace ``NETWORKING_CILIUM_DBPASS`` with a suitable password.

   * Exit the database access client.

     .. code-block:: none

        exit;

#. Source the ``admin`` credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. To create the service credentials, complete these steps:

   * Create the ``networking_cilium`` user:

     .. code-block:: console

        $ openstack user create --domain default --password-prompt networking_cilium

   * Add the ``admin`` role to the ``networking_cilium`` user:

     .. code-block:: console

        $ openstack role add --project service --user networking_cilium admin

   * Create the networking_cilium service entities:

     .. code-block:: console

        $ openstack service create --name networking_cilium --description "networking-cilium" networking-cilium

#. Create the networking-cilium service API endpoints:

   .. code-block:: console

      $ openstack endpoint create --region RegionOne \
        networking-cilium public http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        networking-cilium internal http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        networking-cilium admin http://controller:XXXX/vY/%\(tenant_id\)s
