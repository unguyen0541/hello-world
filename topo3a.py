"""Custom topology example

   Two directly connected switches plus a host for each switch:

      host --- switch --- switch --- host

   Adding the 'topos' dict with a key/value pair to generate our newly defined
   topology enables one to pass in '--topo=mytopo' from the command line.
   """

from mininet.topo import Topo

class RingTopo( Topo ):
       "Simple topology example."

       def __init__( self ):
           "Create custom topo."

           # Initialize topology
           Topo.__init__( self )

           # Add hosts and switches
           h1Host = self.addHost( 'h1' )
           h2Host = self.addHost( 'h2' )
           h3Host = self.addHost( 'h3' )
           h4Host = self.addHost( 'h4' )
           h5Host = self.addHost( 'h5' )
           h6Host = self.addHost( 'h6' )
           s1Switch = self.addSwitch( 's1' )
           s2Switch = self.addSwitch( 's2' )
           s3Switch = self.addSwitch( 's3' )
         

           # Add links
           self.addLink( h1Host, s1Switch )
           self.addLink( h2Host, s1Switch )
           self.addLink( h3Host, s2Switch )
           self.addLink( h4Host, s2Switch )
           self.addLink( h5Host, s3Switch )
           self.addLink( h6Host, s3Switch )
           self.addLink( s1Switch, s2Switch )
           self.addLink( s2Switch, s3Switch )
           self.addLink( s1Switch, s3Switch )


topos = { 'ringtopo': ( lambda: ringTopo() ) }
