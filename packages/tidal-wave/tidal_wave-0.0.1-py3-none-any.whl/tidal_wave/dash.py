#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import json
import re
from typing import Literal, Optional
from xml.etree import ElementTree as ET

import dataclass_wizard

from models import TracksEndpointStreamResponseJSON

Manifest = Union[JSONDASHManifest, XMLDASHManifest]


class TidalManifestException(Exception):
  pass


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
class JSONDASHManifest:
  mime_type: Optional[str] = field(default=None)
  codecs: Optional[str] = field(default=None)
  encryptionType: Optional[str] = field(default=None)
  urls: Optional[List[str]] = field(repr=False, default=None)
  

@dataclass
class XMLDASHManifest:
  mime_type: Optional[str] = field(default=None)
  codecs: Optional[str] = field(default=None)
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


def manifester(tesrj: TracksEndpointStreamResponseJSON) -> Manifest:
  """Attempt to return a Manifest-type object based on
  the attributes of `tesrj`. Will raise TidalManifestException upon
  error"""
  # TODO: another branch for 360 Reality Audio
  if tesrj.manifest_mime_type == "application/vnd.tidal.bts":
    if tesrj.audio_mode == "DOLBY_ATMOS":
      try:
        tm: Manifest = dataclass_wizard.fromdict(
          JSONDASHManifest, json.loads(tesrj.manifest_bytes)
        )
      except json.decoder.JSONDecodeError:
        raise TidalManifestException(
          "Cannot parse manifest with type application/vnd.tidal.bts as JSON"
        )
      except dataclass_wizard.errors.ParseError as pe:
        raise TidalManifestException(pe.message.split("\n")[0])
      else:
        if tm.encryptionType != "NONE":
          raise TidalManifestException(
            f"Manifest for Dolby Atmos track {tesrj.track_id} is encrypted"
          )
        else:
          return tm
    elif tesrj.audio_mode == "STEREO" and tesrj.audio_quality == "HI_RES":
      # Dealing with MQA here
      try:
        tm: Manifest = dataclass_wizard.fromdict(
          JSONDASHManifest, json.loads(tesrj.manifest_bytes)
        )
      except json.decoder.JSONDecodeError:
        raise TidalManifestException(
          "Cannot parse manifest with type application/vnd.tidal.bts as JSON"
        )
      except dataclass_wizard.errors.ParseError as pe:
        raise TidalManifestException(pe.message.split("\n")[0])
      else:
        if tm.encryptionType != "NONE":
          raise TidalManifestException(
            f"Manifest for MQA track {tesrj.track_id} is encrypted"
          )
        else:
          return tm
    else:
      raise TidalManifestException(
        f"Expected a manifest for Dolby Atmos or MQA for track {tesrj.track_id}"
      )
  elif tesrj.manifest_mime_type == "application/dash+xml":
    try:
      xml: ET.Element = ET.fromstring(tesrj.manifest_bytes)
    except ET.ParseError:
      raise TidalManifestException(
        f"Expected an XML manifest for track {tesrj.track_id}"
      )

    ns: str = re.match(r"({.*})", xml.tag).groups()[0]
    st: SegmentTimeline = SegmentTimeline(
      tuple(
        S(**el.attrib)
        if el is not None else None 
        for el in xml.findall(f".//{ns}S")
      )
    )
    
    tm = XMLDASHManifest(
      xml.find(f".//{ns}AdaptationSet").get("mimeType"),
      xml.find(f".//{ns}Representation").get("codecs"),
      xml.find(f".//{ns}AdaptationSet").get("contentType"),
      xml.find(f".//{ns}Representation").get("bandwidth"),
      xml.find(f".//{ns}Representation").get("audioSamplingRate"),
      xml.find(f".//{ns}SegmentTemplate").get("timescale"),
      xml.find(f".//{ns}SegmentTemplate").get("initialization"),
      xml.find(f".//{ns}SegmentTemplate").get("media"),
      xml.find(f".//{ns}SegmentTemplate").get("startNumber"),
      st
    )
    return tm
