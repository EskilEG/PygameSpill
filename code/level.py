from settings import *
from sprites import Sprite, AnimatedSprite, MovingSprite, Item, ParticleEffectSprite
from player import Player
from groups import AllSprites
from random import uniform

class Level:
	def __init__(self, tmx_map, level_frames, data, switch_stage):
		self.display_surface = pygame.display.get_surface()
		self.data = data
		self.switch_stage = switch_stage

		# level data
		self.level_width = tmx_map.width * TILE_SIZE
		self.level_bottom = tmx_map.height * TILE_SIZE
		tmx_level_properties = tmx_map.get_layer_by_name('Data')[0].properties
		if tmx_level_properties['bg']:
			bg_tile = level_frames['bg_tiles'][tmx_level_properties['bg']]
		else:
			bg_tile = None
			
		# groups
		self.all_sprites = AllSprites(
			width = tmx_map.width, 
			height = tmx_map.height,
			bg_tile = bg_tile,
			top_limit = tmx_level_properties['top_limit'],
			clouds = {'large': level_frames['cloud_large'], 'small': level_frames['cloud_small']},
			horizon_line = tmx_level_properties['horizon_line'])
		self.collision_sprites = pygame.sprite.Group()
		self.semi_collision_sprites = pygame.sprite.Group()
		self.damage_sprites = pygame.sprite.Group()
		self.item_sprites = pygame.sprite.Group()

		self.setup(tmx_map, level_frames)

		self.particle_frames = level_frames['particle']

	def setup(self, tmx_map, level_frames):
		#tiles
		for layer in ['BG', 'Terrain', 'FG', 'Platforms']:
			for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
				groups = [self.all_sprites]
				if layer == 'Terrain': groups.append(self.collision_sprites)
				if layer == 'Platforms': groups.append(self.semi_collision_sprites)
				match layer:
					case 'BG': z = Z_LAYERS['bg tiles']
					case 'FG': z = Z_LAYERS['bg tiles']
					case _: z = Z_LAYERS['main']
				Sprite((x * TILE_SIZE,y * TILE_SIZE), surf, groups, z)

		#bg details
		for obj in tmx_map.get_layer_by_name('BG details'):
			if obj.name == 'static':
				Sprite((obj.x, obj.y), obj.image, self.all_sprites, z = Z_LAYERS['bg tiles'])
			elif obj.name == 'candle':
				AnimatedSprite((obj.x, obj.y), level_frames[obj.name], self.all_sprites, z = Z_LAYERS['bg tiles'], animation_speed = ANIMATION_SPEED)

		#objects
		for obj in tmx_map.get_layer_by_name('Objects'):
			if obj.name == 'player': 
				self.player = Player(
					pos = (obj.x, obj.y),
					groups = self.all_sprites, 
					collision_sprites = self.collision_sprites, 
					semi_collision_sprites = self.semi_collision_sprites,
					frames = level_frames['player'],
					data = self.data)

			else:

				if obj.name in ('barrel', 'crate'):
					Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
				else:
					# frames
					frames = level_frames[obj.name] if not 'palm' in obj.name else level_frames['palms'][obj.name]
					if obj.name == 'floor_spike' and obj.properties['inverted']:
						frames = [pygame.transform.flip(frame, False, True) for frame in frames]
					# groups
					groups = [self.all_sprites]
					if obj.name in('palm_small', 'palm_large'): groups.append(self.semi_collision_sprites)

					if obj.name in ('saw', 'floor_spike'): groups.append(self.damage_sprites)

					# z index
					z = Z_LAYERS['main'] if not 'bg' in obj.name else Z_LAYERS['bg details']

					# animation speed
					animation_speed = ANIMATION_SPEED if not 'palm' in obj.name else ANIMATION_SPEED + uniform(-1,1)

					AnimatedSprite((obj.x, obj.y), frames, groups, z, animation_speed)
					
			if obj.name == 'flag':
				self.level_finish_rect = pygame.FRect((obj.x, obj.y), (obj.width, obj.height))
		
		#moving objects
		for obj in tmx_map.get_layer_by_name('Moving Objects'):
			if obj.name == 'spike':
				pass
			else:
				frames = level_frames[obj.name]
				groups = (self.all_sprites, self.semi_collision_sprites) if obj.properties['platform'] else (self.all_sprites, self.damage_sprites)
				if obj.width > obj.height: #horizontal
					move_dir = 'x'
					start_pos = (obj.x, obj.y + obj.height / 2)
					end_pos = (obj.x + obj.width, obj.y + obj.height / 2)
				else: #vertical
					move_dir = 'y'
					start_pos = (obj.x + obj.width / 2, obj.y)
					end_pos = (obj.x + obj.width / 2, obj.y + obj.height)
				speed = obj.properties['speed']
				MovingSprite(frames, groups, start_pos, end_pos, move_dir, speed)
		
		#items
		for obj in tmx_map.get_layer_by_name('Items'):
			Item(obj.name, (obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), level_frames['items'][obj.name], (self.all_sprites, self.item_sprites), self.data)

		#water
		for obj in tmx_map.get_layer_by_name('Water'):
			rows = int(obj.height / TILE_SIZE)
			cols = int(obj.width / TILE_SIZE)
			for row in range(rows):
				for col in range(cols):
					x = obj.x + col * TILE_SIZE
					y = obj.y + row * TILE_SIZE
					if row == 0:
						AnimatedSprite((x, y), level_frames['water_top'], self.all_sprites, Z_LAYERS['water'])
					else:
						Sprite((x, y), level_frames['water_body'], self.all_sprites, Z_LAYERS['water'])

	def hit_collision(self):
		for sprite in self.damage_sprites:
			if sprite.rect.colliderect(self.player.hitbox_rect):
				self.player.get_damage()			

	def item_collision(self):
		if self.item_sprites:
			item_sprites = pygame.sprite.spritecollide(self.player, self.item_sprites, True)
			if item_sprites:
				item_sprites[0].activate() 
				ParticleEffectSprite((item_sprites[0].rect.center), self.particle_frames, self.all_sprites)
				
	def check_constraint(self):
		# left right
		if self.player.hitbox_rect.left <= 0:
			self.player.hitbox_rect.left = 0
		if self.player.hitbox_rect.right >= self.level_width:
			self.player.hitbox_rect.right = self.level_width
		
		# bottom
		if self.player.hitbox_rect.bottom > self.level_bottom or self.data.health == 0:
			self.switch_stage('death')

		# success
		if self.player.hitbox_rect.colliderect(self.level_finish_rect):
			self.switch_stage('win')

	def run(self, dt):
		self.display_surface.fill('black')
		self.all_sprites.update(dt)
		self.hit_collision()
		self.item_collision()
		self.check_constraint()
		self.all_sprites.draw(self.player.hitbox_rect.center, dt)

	
		
		
