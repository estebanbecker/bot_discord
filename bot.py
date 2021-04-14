from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from random import randint
import discord

engine=create_engine('sqlite:///bot.db',echo=True)
Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

class messagesql(Base):
    __tablename__= 'nbrmsg'
    
    id=Column(Integer,primary_key=True)
    nbr=Column(Integer)
    userid=Column(Integer)
    lvl=Column(Integer)
    xp=Column(Integer)
    srvid=Column(Integer)
    username=Column(String)
    lastemsg=Column(Integer)

class lvlroles(Base):
    __tablename__= 'lvlrole'
    
    id=Column(Integer,primary_key=True)
    srvlvlid=Column(Integer)
    roleid1=Column(Integer)
    rolename1=Column(String)
    lvl1=Column(Integer)
    roleid2=Column(Integer)
    rolename2=Column(String)
    lvl2=Column(Integer)
    roleid3=Column(Integer)
    rolename3=Column(String)
    lvl3=Column(Integer)
    roleid4=Column(Integer)
    rolename4=Column(String)
    lvl4=Column(Integer)
    roleid5=Column(Integer)
    rolename5=Column(String)
    lvl5=Column(Integer)

Base.metadata.create_all(engine)
session.commit()

class RoleToAdd:
    id = 1
    name = 'a'

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        usermsg = session.query(messagesql).filter_by(userid=message.author.id,srvid=message.guild.id).first()
        if usermsg==None:
            usermsg=messagesql(nbr=1,userid=message.author.id,lvl=0,xp=randint(10,20),srvid=message.guild.id,username=message.author.name,lastemsg=message.created_at.minute)
        
            session.add(usermsg)
            session.commit()
       
        elif message.created_at.minute != usermsg.lastemsg:
            usermsg.nbr=usermsg.nbr+1
            usermsg.xp=usermsg.xp+randint(10,20)
            usermsg.username=message.author.name
            usermsg.lastemsg=message.created_at.minute
        
            lvl=0
            comparateur=200
            
            while usermsg.xp>comparateur:
                
                lvl=lvl+1
                comparateur=int(((200*(1-1.1**lvl))//(1-1.1)))
        
            if lvl != usermsg.lvl:
                
                usermsg.lvl=lvl
                await message.channel.send('Bravo '+ message.author.display_name+', tu es passé niveau '+str(usermsg.lvl))
                msgdel=await message.channel.history().get(author__name=self.user.name)
                await msgdel.delete(delay=30)
                
                
                level=session.query(lvlroles).filter_by(srvlvlid=message.guild.id).first()
                session.commit()
                
                if lvl >= level.lvl1:
                    
                    RoleToAdd.id=level.roleid1
                    RoleToAdd.name=level.rolename1
                    await message.author.add_roles(RoleToAdd)
                
                if lvl >= level.lvl2:
                    
                    RoleToAdd.id=level.roleid2
                    RoleToAdd.name=level.rolename2
                    await message.author.add_roles(RoleToAdd)
                
                if lvl >= level.lvl3:
                    
                    RoleToAdd.id=level.roleid3
                    RoleToAdd.name=level.rolename3
                    await message.author.add_roles(RoleToAdd)
                
                if lvl >= level.lvl4:
                    
                    RoleToAdd.id=level.roleid4
                    RoleToAdd.name=level.rolename4
                    await message.author.add_roles(RoleToAdd)
                
                if lvl >= level.lvl5:
                    
                    RoleToAdd.id=level.roleid5
                    RoleToAdd.name=level.rolename5
                    await message.author.add_roles(RoleToAdd)
            
            session.add(usermsg)
            session.commit()
            
        
        
        if message.content == '!msg':
            await message.channel.send('Tu as envoyé au total '+ str(usermsg.nbr)+' messages')
            msgdel=await message.channel.history().get(author__name=self.user.name)
            await msgdel.delete(delay=30)
            await message.delete(delay=30)
        
        elif message.content == '!lvl':
            await message.channel.send('Tu es niveau '+ str(usermsg.lvl))
            msgdel=await message.channel.history().get(author__name=self.user.name)
            await msgdel.delete(delay=30)
            await message.delete(delay=30)
        
        elif message.content == '!xp':
            await message.channel.send('Tu a '+ str(usermsg.xp)+'xp')
            msgdel=await message.channel.history().get(author__name=self.user.name)
            await msgdel.delete(delay=30)
            await message.delete(delay=30)
        
        elif message.content == '!fdp':
            await message.channel.send ('Je vous retourne le compliment')
        
        elif message.content =="!nextlvl":
            nextlvl=usermsg.lvl+1
            await message.channel.send ('Il faut '+ str(int(((200*(1-1.1**nextlvl))//(1-1.1))))+ 'xp pour atteindre le niveau '+ str(nextlvl) +', et tu as '+ str(usermsg.xp) +'xp')
            msgdel=await message.channel.history().get(author__name=self.user.name)
            await msgdel.delete(delay=30)
            await message.delete(delay=30)
        elif message.content == '!clearrole':
            level=session.query(lvlroles).filter_by(srvlvlid=message.guild.id).first()
            session.delete(level)
            session.commit()
            await message.channel.send ('Les affectations de rôles par rapport aux niveaux ont été supprimé')
        
        
        if '!maprole' in message.content:
            
            if message.author.guild_permissions.administrator == True:
                msg=message.content.split(' ')
                print(msg[0])
                print(msg[1])
                print(msg[2])
                level=session.query(lvlroles).filter_by(srvlvlid=message.guild.id).first()
                try:
                    print(level)
                    print(level.lvl1)
                    print(level.lvl5)
                except:
                    pass
                
                if level == None:
                    
                    level=lvlroles(srvlvlid=message.guild.id,lvl1=-1,lvl2=-1,lvl3=-1,lvl4=-1,lvl5=-1)
                    
                    session.add(level)
                    session.commit()
                
                if level.lvl1 == -1:
                    
                    try:
                        level.lvl1=int(msg[1])
                        level.roleid1=int(message.role_mentions[0].id)
                        level.rolename1=str(message.role_mentions[0].name)
                        
                        session.add(level)
                        session.commit()
                        
                        await message.channel.send('Le 1er role à bien été set')
                    
                    except:
                        await message.channel.send('Merci d utiliser la forme: !maprole *lvl* *mention du role*')
                        return
                
                elif level.lvl2 == -1:
                    
                    try:
                        print('je suis à 2')
                        level.lvl2=int(msg[1])
                        print('a')
                        level.roleid2=int(message.role_mentions[0].id)
                        print('b')
                        level.rolename2=str(message.role_mentions[0].name)
                        print('c')
                        
                        session.add(level)
                        session.commit()
                    
                        await message.channel.send('Le 2ème role à bien été set')
                    
                    except:
                        await message.channel.send('Merci d utiliser la forme: !maprole *lvl* *mention du role*')
                        return
                
                elif level.lvl3 == -1:
                    
                    try:
                        level.lvl3=int(msg[1])
                        level.roleid3=int(message.role_mentions[0].id)
                        level.rolename3=str(message.role_mentions[0].name)
                        
                        session.add(level)
                        session.commit()
                        
                        await message.channel.send('Le 3ème role à bien été set')
                    
                    except:
                        await message.channel.send('Merci d utiliser la forme: !maprole *lvl* *mention du role*')
                        return
                
                elif level.lvl4 == -1:
                    
                    try:
                        level.lvl4=int(msg[1])
                        level.roleid4=int(message.role_mentions[0].id)
                        level.rolename4=str(message.role_mentions[0].name)
                        
                        session.add(level)
                        session.commit()
                        
                        await message.channel.send('Le 4ème role à bien été set')
                    
                    except:
                        await message.channel.send('Merci d utiliser la forme: !maprole *lvl* *mention du role*')
                        return
                
                elif level.lvl5 == -1:
                    
                    try:
                        level.lvl5=int(msg[1])
                        level.roleid5=int(message.role_mentions[0].id)
                        level.rolename5=str(message.role_mentions[0].name)
                        
                        session.add(level)
                        session.commit()
                        
                        await message.channel.send('Le 5ème role à bien été set')
                    
                    except:
                        await message.channel.send('Merci d utiliser la forme: !maprole *lvl* *mention du role*')
                        return
                
                else:
                    message.channel.send('Il ne peut y avoir que 5 roles liés')
            
            else:
                await message.channel.send('Tu dois être admin')
                
                
client = MyClient()
client.run('')