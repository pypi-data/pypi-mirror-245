import base64
from dataclasses import dataclass, field
from datetime import date, datetime
import logging
import re
from typing import List, Literal, Optional, Tuple, Union

import dataclass_wizard
from requests.auth import AuthBase

logger = logging.getLogger(__name__)
IMAGE_URL: str = "https://resources.tidal.com/images/%s.jpg" 
AudioModeType = Literal["STEREO", "DOLBY_ATMOS"]
AudioQualityType = Literal[
  "HI_RES",
  "HI_RES_LOSSLESS",
  "LOSSLESS",
  "DOLBY_ATMOS",
  "HIGH",
  "LOW"
]
ManifestMimeTypeType = Literal["application/vnd.tidal.bts", "application/dash+xml"] 


class TidalManifestException(Exception):
  pass


@dataclass
class TracksEndpointStreamResponseJSON(dataclass_wizard.JSONWizard):
  """Response from the Tidal API's tracks/{TRACKID} stream
  endpoint. The params and headers, if correctly specified, return the
  manifest of the audio to be streamed. The manifest is a base64-encoded
  XML document or JSON object"""
  track_id: int
  audio_mode: AudioModeType
  audio_quality: AudioQualityType
  manifest: str = field(repr=False)
  album_replay_gain: Optional[float] = field(repr=False, default=None)
  album_peak_amplitude: Optional[float] = field(repr=False, default=None)
  track_replay_gain: Optional[float] = field(repr=False, default=None)
  track_peak_amplitude: Optional[float] = field(repr=False, default=None)
  bit_depth: Optional[int] = field(default=None)
  sample_rate: Optional[int] = field(default=None)
  
  
  def __post_init__(self):
    self.manifest_bytes: bytes = base64.b64decode(self.manifest)
 

class BearerAuth(AuthBase):
  """A class to be passed to the `auth` argument in a `requests.Session`
  constructor"""


  def __init__(self, token: str):
    self.token = token


  def __call__(self, r):
    r.headers["Authorization"] = f"Bearer {self.token}"
    return r


@dataclass(frozen=True)
class Client:
  id: int
  name: str
  authorized_for_offline: bool = field(repr=False)
  authorized_for_offline_date: Optional[datetime] = field(repr=False)


@dataclass(frozen=True)
class SessionsEndpointResponseJSON(dataclass_wizard.JSONWizard):
  session_id: str  # UUID4 value, really
  user_id: int
  country_code: str  # 2-digit country code according to some ISO
  channel_id: int
  partner_id: int
  client: "Client"


@dataclass(frozen=True)
class Artist:
  """A musical artist in the reckoning of the Tidal API"""
  id: int
  name: str
  type: str
  picture: Optional[str]
  
  
  def picture_url(self, dimension: int = 320) -> Optional[str]:
    if self.picture is None:
      return
    elif len(self.picture) != 36 or self.picture.count("-") != 4:
      # Should be a UUID
      return
    else:
      _picture = self.picture.replace("-", "/")
      return IMAGE_URL % f"{_picture}/{dimension}x{dimension}"


@dataclass
class MediaMetadata:
  """The sub-object `mediaMetadata` of /tracks and /albums endpoint responses.
  It represents the quality levels available for the album's songs. These
  quality levels are determined by the client device type, the Tidal account
  level, the country code (read: licensing), the device's quality settings,
  and, perhaps, the device's network connectivity conditions."""
  tags: List[str]


@dataclass(frozen=True)
class TrackAlbum:
  id: int
  title: str
  cover: str = field(repr=None)


@dataclass
class TracksEndpointResponseJSON(dataclass_wizard.JSONWizard):
  """Response from the Tidal API, tracks/{TRACKID} endpoint.If the params and
  headers are correctly specified, the API returns metadata of the available
  version of the audio track, including audio quality, track title, ISRC,
  track artists, album, track number, duration, etc."""
  id: int = field(repr=False)
  title: str
  duration: int  # seconds
  replay_gain: float = field(repr=False)
  peak: float = field(repr=False)
  track_number: int
  volume_number: int
  version: Optional[str]
  copyright: str = field(repr=False)
  url: str
  isrc: str = field(repr=False)
  explicit: bool
  audio_quality: str = field(repr=False)
  audio_modes: List[str] = field(repr=False)
  media_metadata: "MediaMetadata"
  artist: "Artist"
  artists: List["Artist"]
  album: "TrackAlbum"


  def __post_init__(self):
    self.name: str = \
      self.title if self.version is None else f"{self.title} ({self.version})"


@dataclass
class AlbumsEndpointResponseJSON(dataclass_wizard.JSONWizard):
  """This dataclass is the `dataclass-wizard`-generated class that represents
  the JSON response from https://api.tidal.com/v1/albums/<ALBUMID>"""
  id: int = field(repr=False)
  title: str
  duration: int
  number_of_tracks: int
  number_of_volumes: int = field(repr=False)
  release_date: date
  copyright: str = field(repr=False)
  type: str
  version: Optional[str]
  url: str
  cover: str = field(repr=False)
  explicit: bool
  upc: Union[int, str]
  audio_quality: str
  audio_modes: List[str]
  media_metadata: "MediaMetadata" = field(repr=False)
  artist: "Artist" = field(repr=False)
  artists: List["Artist"]

  def __post_init__(self):
    self.cover_url: str = IMAGE_URL % f"{self.cover.replace('-', '/')}/1280x1280"


@dataclass(frozen=True)
class SubscriptionEndpointResponseJSONSubscription:
  type: str
  offline_grace_period: int


@dataclass(frozen=True)
class SubscriptionEndpointResponseJSON(dataclass_wizard.JSONWizard):
  start_date: datetime
  valid_until: datetime
  status: str
  subscription: "SubscriptionEndpointResponseJSONSubscription"
  highest_sound_quality: str
  premium_access: bool
  can_get_trial: bool
  payment_type: str
  payment_overdue: bool


@dataclass(frozen=True)
class AlbumsItemsResponseJSONItem:
  """A sub-object of the response from the Tidal API endpoint
  /albums/<ID>/items. It simply denotes the type of item, which is surely
  going to be 'track', and the same object that is returned from the Tidal
  API /tracks endpoint."""
  item: "TracksEndpointResponseJSON"
  type: str  # "track"


@dataclass(frozen=True)
class AlbumsItemsResponseJSON(dataclass_wizard.JSONWizard):
  """This class represents the JSON response from the Tidal API endpoint
  /albums/<ID>/items. It is a list of TracksEndpointResponseJSON objects, 
  with a bit of metadata based on the query parameters (offset and limit;
  i.e. pagination logic)."""
  limit: int = field(repr=None)
  offset: int = field(repr=None)
  total_number_of_items: int
  items: List["AlbumsItemsResponseJSONItem"]


@dataclass(frozen=True)
class Contributor:
  """The response from the Tidal API endpoint /tracks/<ID>/credits is
  an array of objects, one of the attributes of which is modeled by
  this class. It is simply the name of a contributor to a track,
  and possibly the numerical Tidal resource ID of that contributor."""
  name: str
  id: Optional[int] = field(repr=False, default=None)


@dataclass(frozen=True)
class Credit:
  """The response from the Tidal API endpoint /tracks/<ID>/credits is
  an array of objects modeled by this class. It has an attribute,
  `type`, which is one of the roles a person or entity has in the
  creation of a song/album: Composer, Lyricist, Producer, Mixer,
  Engineer, etc. The `contributors` attribute is an array of Name
  and, optionally, Tidal resource ID for the role"""
  type: str
  contributors: List["Contributor"] = field(repr=False)


@dataclass
class TracksCreditsResponseJSON(dataclass_wizard.JSONWizard):
  """The response from the Tidal API endpoint /tracks/<ID>/credits
  is modeled by this class."""
  credits: List["Credit"]

  def get_credit(self, type_: str) -> Optional["Credit"]:
    """Given a contributor type (e.g. Lyricist, Composer),
    go through the `credits` attribute, returning the `Credit` object
    for the given contributor type if it exists"""
    _credit = None
    try:
      _credit = next(c for c in self.credits if c.type == type_)
    except StopIteration:
      logger.debug(f"There are no credits of type {type_} for this track")
    finally:
      return _credit


  def get_contributors(self, type_: str) -> Optional[Tuple[str]]:
    """Given a contributor type (e.g. Lyricist, Composer),
    go through the `credits` attribute: for each Credit
    object in `self.credits`, if there is a Credit with
    `type` attribute matching `type_` argument, then return
    the `name` attribute for each Contributor object in
    `Credit.contributors`"""
    _credit: Optional["Credit"] = self.get_credit(type_)
    if _credit is not None:
      return tuple(c.name for c in _credit.contributors)
    else:
      return


  def __post_init__(self):
    """Try to parse the various Contributors to top-level
    attributes of this class"""
    self.composer: Optional[Tuple[str]] = self.get_contributors("Composer")
    self.engineer: Optional[Tuple[str]] = self.get_contributors("Engineer")
    self.lyricist: Optional[Tuple[str]] = self.get_contributors("Lyricist")
    self.mixer: Optional[Tuple[str]]    = self.get_contributors("Mixer")
    self.producer: Optional[Tuple[str]] = self.get_contributors("Producer")
    self.remixer: Optional[Tuple[str]]  = self.get_contributors("Remixer")


@dataclass(frozen=True)
class TracksLyricsResponseJSON(dataclass_wizard.JSONWizard):
  """The response from the Tidal API endpoint /tracks/<ID>/lyrics
  is modeled by this class."""
  track_id: int
  lyrics_provider: str
  provider_commontrack_id: str
  provider_lyrics_id: str
  lyrics: str
  subtitles: str
  is_right_to_left: bool


class TidalResource:
  """Parent class to subclasses representing different Tidal music
  service objects; e.g. Track, Album. This class is not meant to be
  instantiated itself: rather, its purpose is to pre-populate its
  subclasses with the `match_url` method."""
  def __init__(self, pattern: Optional[str] = None, url: Optional[str] = None):
    self.pattern = pattern
    self.url = url


  def match_url(self) -> Optional[int]:
    _match: re.Match = re.match(self.pattern, self.url)
    try:
      _id: str = _match.groups()[0]
    except AttributeError:
      return
    else:
      return int(_id)


@dataclass
class TidalAlbum(TidalResource):
  url: str


  def __post_init__(self):
    self.pattern: str = \
      r"http(?:s)?://(?:listen\.)?tidal\.com/(?:browse/)?album/(\d{7,9})(?:.*?)?"
    _id = self.match_url()

    if _id is None:
      raise ValueError(f"'{self.url}' is not a valid Tidal album URL")
    else:
      self.tidal_id = _id
      logger.info(f"Tidal album ID parsed from input: {self.tidal_id}")


@dataclass
class TidalTrack(TidalResource):
  url: str


  def __post_init__(self):
    self.pattern: str = \
      r"http(?:s)?://(?:listen\.)?tidal\.com/(?:browse/)?(?:album/\d{7,9}/)?track/(\d{7,9})(?:.*?)?"
    _id = self.match_url()

    if _id is None:
      raise ValueError(f"'{self.url}' is not a valid Tidal track URL")
    else:
      self.tidal_id = _id
      logger.info(f"Tidal track ID parsed from input: {self.tidal_id}")


@dataclass
class TidalPlaylist(TidalResource):
  NotImplemented


@dataclass
class TidalVideo(TidalResource):
  NotImplemented


@dataclass
class S:
  d: str
  r: Optional[str] = field(default=None)

  def __post_init__(self):
    self.d = int(self.d) if self.d is not None else None
    self.r = int(self.r) if self.r is not None else None


@dataclass(frozen=True)
class SegmentTimeline:
  s: Tuple[Optional["S"]]


@dataclass
class TrackManifest:
  mime_type: Optional[str] = field(default=None)
  codecs: Optional[str] = field(default=None)


@dataclass
class JSONDASHManifest(TrackManifest):
  encryptionType: Optional[str] = field(default=None)
  urls: Optional[List[str]] = field(repr=False, default=None)
  

@dataclass
class XMLDASHManifest(TrackManifest):
  content_type: Optional[str] = field(default=None)
  bandwidth: Optional[str] = field(default=None)
  audio_sampling_rate: Optional[str] = field(default=None)
  timescale: Optional[str] = field(default=None)
  initialization: Optional[str] = field(default=None, repr=False)
  media: Optional[str] = field(default=None, repr=False)
  start_number: Optional[str] = field(default=None, repr=False)
  segment_timeline: Optional["SegmentTimeline"] = field(default=None, repr=False)


  def __post_init__(self):
    self.bandwidth = \
      int(self.bandwidth) if self.bandwidth is not None else None
    self.audioSamplingRate = \
      int(self.audio_sampling_rate) if self.audio_sampling_rate is not None else None
    self.timescale = \
      int(self.timescale) if self.timescale is not None else None
    self.startNumber = \
      int(self.start_number) if self.start_number is not None else None
