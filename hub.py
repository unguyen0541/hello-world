# these import statements are the libraries required in order to access the functions we need
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3

# create a class for our app manager called 'L2Switch'
# this means that ryu-manager will register this ryu-app
class L2Switch(app_manager.RyuApp):
  
  # define the OpenFlow version this ryu-app will use
  # here we are saying that we want OpenFlow v1.3 to be used
  OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
  
  # initialization incantation of this class (pass in args to self)
  # these next two lines ask calling function arguments to be passed to the initialization of our application (L2Switch) 
  def __init__(self, *args, **kwargs):
    super(L2Switch, self).__init__(*args, **kwargs)
    
  # The ryu-manager will do the hardwork of recieving OpenFlow packets
  # If one of those packets is a switch features interrogation, the EventOFPSwitchFeatures will be created
  # ryu-manger will call this function because it has been registered for the event EventOFPSwitchFeatures
  # Handle switch feature interrogation event 
  @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
  def switch_features_handler(self, ev):
    # The line below will have the ryu-app do nothing 
    # define shortened variables
    msg = ev.msg
    dp = msg.datapath
    ofp = dp.ofproto
    ofp_parser = dp.ofproto_parser

    # match all packets with priority 0
    match = ofp_parser.OFPMatch()
    pri = 0

    # set action (forward packet to controller)
    actions = [ofp_parser.OFPActionOutput(ofp.OFPP_CONTROLLER, ofp.OFPCML_NO_BUFFER)]

    # set the instruction to apply the action
    # teach switch be smart/learning
    inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]

    # formulate the final openflow packet
    mod = ofp_parser.OFPFlowMod(datapath=dp, priority=pri, match=match, instructions=inst)

    # install the table-miss flow entry.
    dp.send_msg(mod)    

  
  # Handle switch packet in event
  # the @ is the declarite
  @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
  def packet_in_handler(self, ev):
    # register values into shorter variable names
    # take all the data/header stuff, port and send it out 
    msg = ev.msg
    dp = msg.datapath
    ofp = dp.ofproto
    ofp_parser = dp.ofproto_parser

    # create flood action
    actions = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]

    # create response to packetin
    # green tree is here. It give the action for packageOut
    out = ofp_parser.OFPPacketOut(
                     datapath=dp,
                     buffer_id=msg.buffer_id,
                     in_port=msg.match['in_port'],
                     actions=actions
         )

    # actually send the packet to the requesting switch
    # This python is not very effectively because, switch keeps 
    # raise/send message to controller to ask for me 
    dp.send_msg(out)
