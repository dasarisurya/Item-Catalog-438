from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Club, Base, TeamPlayer, User
 
engine = create_engine('sqlite:///footballclubs.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
''' A DBSession() instance establishes all conversations with the database
    and represents a "staging zone" for all the objects loaded into the
    database session object. Any change made against the objects in the
    session won't be persisted into the database until you call
    session.commit(). You can revert all of them back to the last commit by
    calling session.rollback()
''' 
session = DBSession()

# create a user
# User's name and email is given
User1 = User(name="Surya Dasari", email="dasaridinesh5@gmail.com")

# Team for Barcelona
club1 = Club(name = "Barcelona")

session.add(club1)
session.commit()

# commits are done

# Team players are added here

teamPlayer1 = TeamPlayer(name = "Lionel Messi", description = "Argentine professional footballer who plays as a forward for Spanish club Barcelona and the Argentine national team. Often considered the best player in the world.", price = "$2.99", course = "Striker", club = club1)

session.add(teamPlayer1)
session.commit()

teamPlayer2 = TeamPlayer(name = "Luis Suarez", description = "Uruguayan professional footballer who plays as a striker for Spanish club Barcelona and the Uruguay national team.", price = "$5.50", course = "Striker", club = club1)

session.add(teamPlayer2)
session.commit()

teamPlayer3 = TeamPlayer(name = "Sergi Roberto", description = "Spanish professional footballer who plays for Barcelona. Mainly a full-back, he can also operate as a central midfielder, defensive midfielder or winger.", price = "$3.99", course = "MidFielder", club = club1)

session.add(teamPlayer3)
session.commit()

teamPlayer4 = TeamPlayer(name = "Phil Coutinho", description = "Brazilian professional footballer who plays as an attacking midfielder or winger for Spanish club Barcelona and the Brazilian national team.", price = "$7.99", course = "MidFielder", club = club1)

session.add(teamPlayer4)
session.commit()

teamPlayer5 = TeamPlayer(name = "Gerard Pique", description = "Spanish professional footballer who plays as a centre-back for Barcelona and the Spain national team.", price = "$1.99", course = "Defender", club = club1)

session.add(teamPlayer5)
session.commit()

teamPlayer6 = TeamPlayer(name = "Samuel Umtiti", description = "French professional footballer who plays as a centre-back for Spanish club Barcelona and the France national team", price = "$.99", course = "Defender", club = club1)

session.add(teamPlayer6)
session.commit()

teamPlayer7 = TeamPlayer(name = "Marc Andre Terstegen", description = "German professional footballer who plays as a goalkeeper for Spanish club Barcelona and the German national team.", price = "$3.49", course = "GoalKeeper", club = club1)

session.add(teamPlayer7)
session.commit()


# Team for Real Madrid
club2 = Club(name = "Real Madrid")

session.add(club2)
session.commit()

# commits are done

# Team players are added here

teamPlayer1 = TeamPlayer(name = "Gerath Bale", description = "Welsh professional footballer who plays as a winger for Spanish club Real Madrid and the Wales national team.", price = "$7.99", course = "Striker", club = club2)

session.add(teamPlayer1)
session.commit()

teamPlayer2 = TeamPlayer(name = "C Portuguese professional footballer who plays as a forward for Spanish club Real Madrid and the Portugal national team.ristiano Ronaldo", description = "", price = "$25", course = "Striker", club = club2)

session.add(teamPlayer2)
session.commit()

teamPlayer3 = TeamPlayer(name = "Luca Modric", description = "Croatian professional footballer who plays for Spanish club Real Madrid and captains the Croatia national team.", price = "15", course = "MidFielder", club = club2)

session.add(teamPlayer3)
session.commit()

teamPlayer4 = TeamPlayer(name = "Toni Kroos", description = "German professional footballer who plays as a midfielder for Spanish club Real Madrid and the German national team.", price = "12", course = "MidFielder", club = club2)

session.add(teamPlayer4)
session.commit()

teamPlayer5 = TeamPlayer(name = "Sergi Ramos", description = "Spanish professional footballer who plays for and captains both Real Madrid and the Spain national team. Primarily a central defender, he can also play as a right back.", price = "14", course = "Defender", club = club2)

session.add(teamPlayer5)
session.commit()

teamPlayer6 = TeamPlayer(name = "Keylor Navas", description = "Costa Rican professional footballer who plays as a goalkeeper for Spanish club Real Madrid and the Costa Rica national team.", price = "12", course = "GoalKeeper", club = club2)

session.add(teamPlayer6)
session.commit()


#Team for Paris Saint Germain
club1 = Club(name = "Paris Saint Germain")

session.add(club1)
session.commit()

# commits are done

# Team players are added here

teamPlayer1 = TeamPlayer(name = "Neymar Junior", description = "Brazilian professional footballer who plays as a forward for French club Paris Saint-Germain and the Brazil national team.", price = "$8.99", course = "Striker", club = club1)

session.add(teamPlayer1)
session.commit()

teamPlayer2 = TeamPlayer(name = "Mbappe", description = " French professional footballer who plays as a forward for Paris Saint-Germain, on loan from fellow Ligue 1 club Monaco, and the France national team.", price = "$6.99", course = "Striker", club = club1)

session.add(teamPlayer2)
session.commit()

teamPlayer3 = TeamPlayer(name = "Dani Alves", description = "Brazilian professional footballer who plays as a right back for French club Paris Saint-Germain and the Brazil national team.", price = "$9.95", course = "MidFielder", club = club1)

session.add(teamPlayer3)
session.commit()

teamPlayer4 = TeamPlayer(name = "Angel Di Maria", description = "Argentine professional footballer who plays for Ligue 1 club Paris Saint-Germain and the Argentina national team.", price = "$6.99", course = "MidFielder", club = club1)

session.add(teamPlayer4)
session.commit()

teamPlayer2 = TeamPlayer(name = "Kevin Trapp", description = "German professional footballer who plays as a goalkeeper for Paris Saint-Germain and the Germany national team.", price = "$9.50", course = "GoalKeeper", club = club1)

session.add(teamPlayer2)
session.commit()


#Team for Liverpool
club1 = Club(name = "Liverpool")

session.add(club1)
session.commit()

# commits are done

# Team players are added here

teamPlayer1 = TeamPlayer(name = "Mohammed Salah", description = "Egyptian professional footballer who plays as a forward for English club Liverpool and the Egyptian national team.", price = "$2.99", course = "Striker", club = club1)

session.add(teamPlayer1)
session.commit()

teamPlayer2 = TeamPlayer(name = "Sadio Mane", description = "Senegalese professional footballer who plays as a winger for Premier League club Liverpool and the Senegal national team.", price = "$5.99", course = "Striker", club = club1)

session.add(teamPlayer2)
session.commit()

teamPlayer3 = TeamPlayer(name = "James Milner", description = "English professional footballer who plays for Premier League club Liverpool. A versatile player, he has been used in many different positions such as on the wing, in midfield and at full back.", price = "$4.50", course = "MidFielder", club = club1)

session.add(teamPlayer3)
session.commit()

teamPlayer4 = TeamPlayer(name = "Ragnar Klavan", description = "Estonian professional footballer who plays as a defender for Premier League club Liverpool and captains the Estonia national team.", price = "$6.95", course = "Defender", club = club1)

session.add(teamPlayer4)
session.commit()

teamPlayer5 = TeamPlayer(name = "Simon Mignolet", description = "Belgian professional footballer who plays as a goalkeeper for Premier League club Liverpool and the Belgium national team.", price = "$7.95", course = "GoalKeeper", club = club1)

session.add(teamPlayer5)
session.commit()


# Team for Bayern Munchen
club1 = Club(name = "Bayern Munchen")

session.add(club1)
session.commit()

# commits are done

# Team players are added here

teamPlayer1 = TeamPlayer(name = "Arjen Robben", description = "Dutch professional footballer who plays for German club Bayern Munich.", price = "$13.95", course = "MidFielder", club = club1)

session.add(teamPlayer1)
session.commit()

teamPlayer2 = TeamPlayer(name = "Robert Lewandowski", description = "Polish professional footballer who plays as a striker for Bundesliga club Bayern Munich and is the captain of the Poland national team.", price = "$4.95", course = "Striker", club = club1)

session.add(teamPlayer2)
session.commit()

teamPlayer3 = TeamPlayer(name = "James Roudriguez", description = "Colombian professional footballer who plays as an attacking midfielder or winger for German club Bayern Munich.", price = "$6.95", course = "Striker", club = club1)

session.add(teamPlayer3)
session.commit()

teamPlayer4 = TeamPlayer(name = "David Alaba", description = "Austrian professional footballer who plays for German club Bayern Munich and the Austria national team.", price = "$3.95", course = "Defender", club = club1)

session.add(teamPlayer4)
session.commit()

teamPlayer5 = TeamPlayer(name = "Sven Ulreich", description = "German professional footballer who plays as a goalkeeper for Bundesliga side Bayern Munich.", price = "$7.95", course = "GoalKeeper", club = club1)

session.add(teamPlayer5)
session.commit()


# Team for Juventus 
club1 = Club(name = "Juventus")

session.add(club1)
session.commit()

# commits are done

# Team players are added here

teamPlayer1 = TeamPlayer(name = "Douglas Costa", description = "Brazilian footballer who plays as a winger for Italian club Juventus and the Brazil national team.", price = "$9.95", course = "Defender", club = club1)

session.add(teamPlayer1)
session.commit()

teamPlayer2 = TeamPlayer(name = "Sami Khedria", description = "German professional footballer who plays as a central midfielder for Juventus and the Germany national team.", price = "$7.95", course = "MidFielder", club = club1)

session.add(teamPlayer2)
session.commit()

teamPlayer3 = TeamPlayer(name = "Paulo Dybala", description = "Argentine professional footballer who plays as a forward for Italian club Juventus and the Argentina national team.", price = "$6.50", course = "Striker", club = club1)

session.add(teamPlayer3)
session.commit()

teamPlayer4 = TeamPlayer(name = "Buffon", description = "Italian professional footballer who plays as a goalkeeper for Juventus.", price = "$6.75", course = "GoalKeeper", club = club1)

session.add(teamPlayer4)
session.commit()



# Team for Manchester City
club1 = Club(name = "Manchester City")

session.add(club1)
session.commit()

# commits are done

# Team players are added here

teamPlayer1 = TeamPlayer(name = "Danilo", description = "Brazilian professional footballer who plays for English club Manchester City as a right or left-back.", price = "$2.99", course = "Defender", club = club1)

session.add(teamPlayer1)
session.commit()

teamPlayer2 = TeamPlayer(name = "David Silva", description = "Spanish professional footballer who plays for English club Manchester City and the Spain national team", price = "$10.95", course = "MidFielder", club = club1)

session.add(teamPlayer2)
session.commit()

teamPlayer3 = TeamPlayer(name = "Gabriel Jesus", description = "Brazilian professional footballer who plays as a forward for Premier League club Manchester City and the Brazil national team.", price = "$7.50", course = "Striker", club = club1)

session.add(teamPlayer3)
session.commit()

teamPlayer4 = TeamPlayer(name = "Sergio Aguero", description = "Argentine professional footballer who plays as a striker for Premier League club Manchester City and the Argentine national team.", price = "$7.50", course = "Striker", club = club1)

session.add(teamPlayer4)
session.commit()


print "Team members added!"

