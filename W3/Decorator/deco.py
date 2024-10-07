from abc import ABC, abstractmethod

class AbstractEffect(ABC, Hero):
    def __init__(self, base):
        self.base = base
        self.stats = base.stats
        self.positive_effects = base.positive_effects
        self.negative_effects = base.negative_effects
        
    @abstractmethod
    def get_positive_effects(self):
        pass
    
    @abstractmethod
    def get_negative_effects(self):
        pass

    
class AbstractPositive(AbstractEffect):
    @abstractmethod
    def get_positive_effects(self):
        pass
    
    def get_negative_effects(self):
        return self.base.get_negative_effects()

    
class AbstractNegative(AbstractEffect):
    def get_positive_effect(self):
        return self.base.get_positive_effect()
    
    @abstractmethod
    def get_negative_effects(self):
        return self.base.get_negative_effects()
    
    
class Berserk(AbstractPositive):
    def get_positive_effects(self):
        temp_string = self.base.get_positive_effects()
        temp_string.append('Berserk')
        return temp_string
    
    def get_negative_effects(self):
        return self.base.get_negative_effects()
    
    def get_stats(self):
        stats = self.base.get_stats()
        stats['HP'] += 50
        stats['Strength'] += 7
        stats['Endurance'] += 7
        stats['Agility'] += 7
        stats['Luck'] += 7
        stats['Perception'] -= 3
        stats['Charisma'] -= 3
        stats['Intelligence'] -= 3
        return stats
    
    
class Blessing(AbstractPositive):
    def get_positive_effects(self):
        temp_string = self.base.get_positive_effects()
        temp_string.append('Blessing')
        return temp_string
    
    def get_negative_effects(self):
        return self.base.get_negative_effects()
    
    def get_stats(self):
        stats = self.base.get_stats()
        stats['Strength'] += 2
        stats['Endurance'] += 2
        stats['Agility'] += 2
        stats['Luck'] += 2
        stats['Perception'] += 2
        stats['Charisma'] += 2
        stats['Intelligence'] += 2
        return stats
    
    
class Weakness(AbstractNegative):
    def get_negative_effects(self):
        temp_string = self.base.get_negative_effects()
        temp_string.append('Weakness')
        return temp_string
    
    def get_positive_effects(self):
        return self.base.get_positive_effects()
    
    def get_stats(self):
        stats = self.base.get_stats()
        stats['Strength'] -= 4
        stats['Endurance'] -= 4
        stats['Agility'] -= 4
        return stats
    
    
class EvilEye(AbstractNegative):
    def get_negative_effects(self):
        temp_string = self.base.get_negative_effects()
        temp_string.append('EvilEye')
        return temp_string
    
    def get_positive_effects(self):
        return self.base.get_positive_effects()
    
    def get_stats(self):
        stats = self.base.get_stats()
        stats['Luck'] -= 10
        return stats
    
    
class Curse(AbstractNegative):
    def get_negative_effects(self):
        temp_string = self.base.get_negative_effects()
        temp_string.append('Curse')
        return temp_string
    
    def get_positive_effects(self):
        return self.base.get_positive_effects()
    
    def get_stats(self):
        stats = self.base.get_stats()
        stats['Strength'] -= 2
        stats['Endurance'] -= 2
        stats['Agility'] -= 2
        stats['Luck'] -= 2
        stats['Perception'] -= 2
        stats['Charisma'] -= 2
        stats['Intelligence'] -= 2
        return stats