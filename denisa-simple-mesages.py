import spade





class MyAgent(spade.Agent.Agent):

    class SendBehav(spade.Behaviour.OneShotBehaviour):

        def _process(self):

            # First, form the receiver AID

            receiver = spade.AID.aid(name="receiver@127.0.0.1",

                                     addresses=["xmpp://receiver@127.0.0.1"])



            # Second, build the message

            self.msg = spade.ACLMessage.ACLMessage()  # Instantiate the message

            self.msg.setPerformative("inform")  # Set the "inform" FIPA performative

            self.msg.setOntology("cooking")  # Set the ontology of the message content

            self.msg.setLanguage("OWL-S")  # Set the language of the message content

            self.msg.addReceiver(receiver)  # Add the message receiver

            self.msg.setContent("Hello World")  # Set the message content

            # print self.msg

            # Third, send the message with the "send" method of the agent

            self.myAgent.send(self.msg)



    class ReceiveBehav(spade.Behaviour.Behaviour):

        """This behaviour will receive all kind of messages"""



        def _process(self):

            self.msg = None



            # Blocking receive for 10 seconds

            self.msg = self._receive(True, 10)



            # Check wether the message arrived

            if self.msg:

                print "I got a message!"

            else:

                print "I waited but got no message"



    def _setup(self):

        print "MyAgent starting . . ."

        sb = self.SendBehav()

        rb = self.ReceiveBehav()

        self.setDefaultBehaviour(rb)



        cooking_template = spade.Behaviour.ACLTemplate()

        cooking_template.setOntology("cooking")

        mt = spade.Behaviour.MessageTemplate(cooking_template)



        self.addBehaviour(sb, mt)





if __name__ == "__main__":

    a = MyAgent("agent@127.0.0.1", "secret")

    b = MyAgent("receiver@127.0.0.1", "secret")

    a.start()

    b.start()