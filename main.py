import spade

class MyAgent(spade.Agent.Agent):
    class ReceiveBehav(spade.Behaviour.Behaviour):
        """This behaviour will receive all kind of messages"""

        def _process(self):
            self.msg = None

            # Blocking receive for 10 seconds
            self.msg = self._receive(True, 10)

            # Check wether the message arrived
            if self.msg:
                print "I got a message"
            else:
                print "I waited but got no message"

    class AnotherBehav(spade.Behaviour.Behaviour):
        """This behaviour will receive only messages of the 'cooking' ontology"""

        def _process(self):
            self.msg = None

            # Blocking receive indefinitely
            self.msg = self._receive(True)

            # Check wether the message arrived
            if self.msg:
                print "I got a cooking message!"
            else:
                print "I waited but got no cooking message"

    def _setup(self):
        # Add the "ReceiveBehav" as the default behaviour
        rb = self.ReceiveBehav()
        self.setDefaultBehaviour(rb)

        # Prepare template for "AnotherBehav"
        cooking_template = spade.Behaviour.ACLTemplate()
        cooking_template.setOntology("cooking")
        mt = spade.Behaviour.MessageTemplate(cooking_template)

        ab = self.AnotherBehav()
        # Add the behaviour WITH the template
        self.addBehaviour(ab, mt)


class MyAgent_send(spade.Agent.Agent):
    class InformBehav(spade.Behaviour.Behaviour):
        def _process(self):
            # First, form the receiver AID
            receiver = spade.AID.aid(name="agent@127.0.0.1",
                                     addresses=["xmpp://agent@127.0.0.1"])

            # Second, build the message
            self.msg = spade.ACLMessage.ACLMessage()  # Instantiate the message
            self.msg.setPerformative("inform")  # Set the "inform" FIPA performative
            self.msg.setOntology("test")  # Set the ontology of the message content
            self.msg.setLanguage("OWL-S")  # Set the language of the message content
            self.msg.addReceiver(receiver)  # Add the message receiver
            self.msg.setContent("Hello World")  # Set the message content
            # Third, send the message with the "send" method of the agent
            self.myAgent.send(self.msg)


    def _setup(self):
        print "MyAgent starting . . ."
        b = self.InformBehav()
        self.addBehaviour(b, None)


if __name__ == "__main__":
    a = MyAgent("agent@127.0.0.1", "secret")
    a_send = MyAgent_send("as@127.0.0.1", "secret")
    a.start()
    a_send.start()
